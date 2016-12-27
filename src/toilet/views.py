import json

from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from channels import Group
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import ToiletLectureSerializer
from .models import ToiletLecture, Toilet


class ToiletStatusView(TemplateView):
    template_name = 'toilet_status.html'

    def get_context_data(self, **kwargs):
        context = super(ToiletStatusView, self).get_context_data(**kwargs)
        context['toilets'] = Toilet.objects.all()
        return context


class ToiletLastEventView(View):

    def get(self, request, *args, **kwargs):
        Group("stream").send({"text": json.dumps(ToiletLecture.last_lecture())})
        return HttpResponse()


class ToiletLectureCreateAPIView(generics.CreateAPIView):
    model = ToiletLecture
    serializer_class = ToiletLectureSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(None, status=status.HTTP_201_CREATED, headers=headers)


class ToiletLastLectureView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return Response(ToiletLecture.last_lecture())
