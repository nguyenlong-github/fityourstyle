# from django.shortcuts import render
# from django.views import View
# from .models import Appointment, User, Store
# from datetime import datetime, timedelta
# from .forms import AppointmentForm
# from django.contrib.auth.mixins import LoginRequiredMixin



# # HomePageView
# class HomePageView(View):
#     def get(self, request):
#         return render(request, 'myapp/home_page.html')
        
# # FaceShapeCheckView
# class FaceShapeCheckView(View):
#     def get(self, request):
#         return render(request, 'myapp/face_shape_check.html')

# # HairStyleSuggestionsView
# class HairStyleSuggestionsView(View):
#     def get(self, request):
#         return render(request, 'myapp/hair_style_suggestions.html')

# # VirtualHairstyleView
# class VirtualHairstyleView(View):
#     def get(self, request):
#         return render(request, 'myapp/virtual_hairstyle.html')

# # AppointmentView
# class AppointmentView(LoginRequiredMixin,View):
#     def get(self, request):
#         form = AppointmentForm()
#         stores = Store.objects.all()  # Lấy tất cả các cửa hàng từ Model Store
        
#         # Nạp dữ liệu dạng string được gửi đến bằng phương thức GET
#         date_str = request.GET.get("appointment-date", None)
#         time_str = request.GET.get("appointment-time", None)
#         store_id = request.GET.get("appointment-store", None)  # Lấy ID của Store từ GET

#         # Kiểm tra xem dữ liệu có được gửi đến không
#         if date_str and time_str and store_id:
#             # Biến đổi dữ liệu từ string -> date và time
#             date = datetime.strptime(date_str, "%Y-%m-%d").date()
#             time = datetime.strptime(time_str, "%H:%M").time()

#             user_datetime = datetime.combine(date, time)
#             end_datetime = user_datetime + timedelta(minutes=30)

#             # Kiểm tra trong Model (database) có tồn tại bản ghi nào chưa
#             is_duplicate = Appointment.objects.filter(
#                 store_id=store_id,  # Kiểm tra cửa hàng
#                 date=date,  # Kiểm tra ngày
#                 time__lt=end_datetime.time(),  # Kiểm tra thời gian
#                 time__gte=(user_datetime - timedelta(minutes=30)).time(),  # Kiểm tra thời gian
#             ).exists()
#             # Kiểm tra xem bản ghi chưa tồn tại trong Model
#             if is_duplicate:
#                 return render(request, 'myapp/appointment.html', {'system_message': "This time slot is already booked", 'end_datetime': end_datetime.time(), 'form': form, 'stores': stores})
#             else:
#                 return render(request, 'myapp/appointment.html', {'system_message': "OK", 'form': form, 'stores': stores})
#         else:
#             return render(request, 'myapp/appointment.html', {'system_message': "Fill date, time, and store please!", 'form': form, 'stores': stores})


#     def post(self, request):
#         form = AppointmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             user_id = "feb5066a-09d6-4263-8cbc-b757ba443915"
#             appointment = form.save(commit=False)
#             appointment.user_id = user_id
#             appointment.save()
#             return render(request, 'myapp/appointment.html', {'system_message': "Appointment submitted successfully!", 'form': form})
#         else:
#             return render(request, 'myapp/appointment.html', {'system_message': "Fill date, time, and store please!", 'form': form})


# class AppointmentManageView(View):
#     def get(self, request):
#         date_str = request.GET.get("date",None)
#         if date_str:
#             try:
#                 date = datetime.strptime(date_str,"%Y-%m-%d").date()
#                 appointment_data = Appointment.objects.filter(date=date)    
#             except ValueError:
#                 appointment_data = [] # Ngay khong hop le
#         else:
#             return render(request, 'myapp/appointment_manage.html')
#         return render(request, 'myapp/appointment_manage.html',{'appointment_data' : appointment_data})






# home_page = HomePageView.as_view()
# face_shape_check = FaceShapeCheckView.as_view()
# hair_style_suggestions = HairStyleSuggestionsView.as_view()
# virtual_hairstyle = VirtualHairstyleView.as_view()
# appointment = AppointmentView.as_view()
# appointment_manage = AppointmentManageView.as_view()

from django.shortcuts import render, redirect
from django.views import View
from .models import Appointment, Store
from datetime import datetime, timedelta
from .forms import AppointmentForm
from django.contrib.auth.mixins import LoginRequiredMixin

# HomePageView
class HomePageView(View):
    def get(self, request):
        return render(request, 'myapp/home_page.html')

# FaceShapeCheckView
class FaceShapeCheckView(View):
    def get(self, request):
        return render(request, 'myapp/face_shape_check.html')

# HairStyleSuggestionsView
class HairStyleSuggestionsView(View):
    def get(self, request):
        return render(request, 'myapp/hair_style_suggestions.html')

# VirtualHairstyleView
class VirtualHairstyleView(View):
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
class AppointmentManageView(View):
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


