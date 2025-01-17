# Import For Web
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Appointment, Store
from datetime import datetime, timedelta
from .forms import AppointmentForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Import For AI
import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


# HomePageView
class HomePageView(View):
    def get(self, request):
        return render(request, 'myapp/home_page.html')

# FaceShapeCheckView
class FaceShapeCheckView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'myapp/face_shape_check3.html')

    def post(self, request):
        if 'image' not in request.FILES:
            return HttpResponseBadRequest("No image file provided.")

        image_file = request.FILES['image']
        image_path = self.save_uploaded_file(image_file)

        try:
            result = self.process_image(image_path)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse(result)

    def save_uploaded_file(self, file):
        upload_dir = 'media/myapp/picture/user_uploads'
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file_path

    def process_image(self, image_path):
        model = tf.keras.models.load_model('ai_model/model.keras')
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Không tìm thấy ảnh tại đường dẫn: {image_path}")

        image_resized = cv2.resize(image, (128, 128))
        image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
        image_normalized = image_resized / 255.0
        image_input = np.expand_dims(image_normalized, axis=0)

        predictions = model.predict(image_input)
        predictions_percentage = predictions[0] * 100
        labels = ['Square', 'Oval', 'Oblong', 'Round', 'Heart']
        predicted_class = np.argmax(predictions, axis=1)
        predicted_label = labels[predicted_class[0]]

        return {
            "predictions": {label: float(percentage) for label, percentage in zip(labels, predictions_percentage)},
            "predicted_label": predicted_label,
        }

# HairStyleSuggestionsView
class HairStyleSuggestionsView(View):
    def get(self, request):
        return render(request, 'myapp/hair_style_suggestions.html')

# VirtualHairstyleView
class VirtualHairstyleView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'myapp/virtual_hairstyle.html')

# AppointmentView
class AppointmentView(LoginRequiredMixin, View):
    def get(self, request):
        form = AppointmentForm()
        stores = Store.objects.all()  # Lấy tất cả các cửa hàng từ Model Store
        
        # Nạp dữ liệu dạng string được gửi đến bằng phương thức GET
        date_str = request.GET.get("appointment-date", None)
        time_str = request.GET.get("appointment-time", None)
        store_id = request.GET.get("appointment-store", None)  # Lấy ID của Store từ GET

        # Kiểm tra xem dữ liệu có được gửi đến không
        if date_str and time_str and store_id:
            # Biến đổi dữ liệu từ string -> date và time
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()

            user_datetime = datetime.combine(date, time)
            end_datetime = user_datetime + timedelta(minutes=30)

            # Kiểm tra trong Model (database) có tồn tại bản ghi nào chưa
            is_duplicate = Appointment.objects.filter(
                store_id=store_id,  # Kiểm tra cửa hàng
                date=date,  # Kiểm tra ngày
                time__lt=end_datetime.time(),  # Kiểm tra thời gian
                time__gte=(user_datetime - timedelta(minutes=30)).time(),  # Kiểm tra thời gian
            ).exists()

            # Kiểm tra xem bản ghi chưa tồn tại trong Model
            if is_duplicate:
                return render(request, 'myapp/appointment.html', {
                    'system_message': "This time slot is already booked",
                    'end_datetime': end_datetime.time(),
                    'form': form,
                    'stores': stores
                })
            else:
                return render(request, 'myapp/appointment.html', {
                    'system_message': "OK",
                    'form': form,
                    'stores': stores
                })
        else:
            return render(request, 'myapp/appointment.html', {
                'system_message': "Fill date, time, and store please!",
                'form': form,
                'stores': stores
            })

    def post(self, request):
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # Sử dụng người dùng đăng nhập hiện tại
            appointment.save()
            return render(request, 'myapp/appointment.html', {
                'system_message': "Appointment submitted successfully!",
                'form': form
            })
        else:
            return render(request, 'myapp/appointment.html', {
                'system_message': "Form is invalid. Please check the details.",
                'form': form
            })

# AppointmentManageView
class AppointmentManageView(LoginRequiredMixin, View):
    def get(self, request):
        date_str = request.GET.get("date", None)
        appointment_data = []

        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                appointment_data = Appointment.objects.filter(date=date)
            except ValueError:
                pass  # Ngày không hợp lệ, không thực hiện gì

        return render(request, 'myapp/appointment_manage.html', {'appointment_data': appointment_data})


# Khai báo views
home_page = HomePageView.as_view()
face_shape_check = FaceShapeCheckView.as_view()
hair_style_suggestions = HairStyleSuggestionsView.as_view()
virtual_hairstyle = VirtualHairstyleView.as_view()
appointment = AppointmentView.as_view()
appointment_manage = AppointmentManageView.as_view()


