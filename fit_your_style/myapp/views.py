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

# VirtualHairstyle Import
from django.http import StreamingHttpResponse
from PIL import Image
import mediapipe as mp
import math

# Virtual Hairstyle View for displaying the page
class VirtualHairstyleView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'myapp/virtual_hairstyle.html')

from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import math

# Khởi tạo một instance của HairFilter để sử dụng chung
class HairFilter:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Load ảnh tóc với PIL và chuyển sang RGBA mode
        self.hair_styles = {}
        try:
            pil_image1 = Image.open('myapp/static/hairstyles/hairstyle1.png').convert('RGBA')
            pil_image2 = Image.open('myapp/static/hairstyles/hairstyle2.png').convert('RGBA')

            # Chuyển từ PIL sang numpy array
            self.hair_styles['style1'] = np.array(pil_image1)
            self.hair_styles['style2'] = np.array(pil_image2)

            print("Loaded images with shapes:", 
                self.hair_styles['style1'].shape,
                self.hair_styles['style2'].shape)
        except Exception as e:
            print(f"Error loading hairstyle images: {e}")

        self.current_style = 'style1'

        # Hệ số điều chỉnh kích thước và vị trí
        self.hair_scale_factors = {'style1': 1.65, 'style2': 2.13}
        self.hair_position_offsets = {
            'style1': {'x_offset': 0, 'y_offset': 4},
            'style2': {'x_offset': -10, 'y_offset': 60}
        }

        self.x_offset = self.hair_position_offsets[self.current_style]['x_offset']
        self.y_offset = self.hair_position_offsets[self.current_style]['y_offset']
        self.scale_factor = self.hair_scale_factors[self.current_style]

    def overlay_image_alpha(self, img, img_overlay, pos, alpha_mask):
        """Chồng một ảnh PNG có alpha channel lên ảnh gốc"""
        x, y = pos
        y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
        x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

        if y1 >= y2 or x1 >= x2:
            return

        img_overlay_crop = img_overlay[y1-y:y2-y, x1-x:x2-x]
        alpha = alpha_mask[y1-y:y2-y, x1-x:x2-x]
        img_crop = img[y1:y2, x1:x2]

        alpha_3d = np.stack([alpha] * 3, axis=2) / 255.0
        comp = img_overlay_crop.astype(float) * alpha_3d + img_crop.astype(float) * (1.0 - alpha_3d)
        img[y1:y2, x1:x2] = comp.astype(np.uint8)

    def calculate_head_tilt_angle(self, face_landmarks):
        """Tính góc nghiêng đầu"""
        temple_left = face_landmarks.landmark[447]
        temple_right = face_landmarks.landmark[227]
        dx = temple_right.x - temple_left.x
        dy = temple_right.y - temple_left.y
        angle = math.atan2(dy, dx) * 180 / math.pi
        return angle

    def apply_hair(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                ih, iw, _ = frame.shape
                head_angle = self.calculate_head_tilt_angle(face_landmarks)

                temple_left = face_landmarks.landmark[447]
                temple_right = face_landmarks.landmark[227]
                top_head = face_landmarks.landmark[10]
                face_width = int(abs(temple_right.x - temple_left.x) * iw * self.scale_factor)
                
                center_x = int((temple_left.x + temple_right.x) * iw / 2) + self.x_offset
                center_y = int(top_head.y * ih) + self.y_offset
                
                hair_img = self.hair_styles[self.current_style]
                if hair_img is not None:
                    scale = face_width / hair_img.shape[1]
                    scaled_hair = cv2.resize(hair_img, None, fx=scale, fy=scale)
                    rotated_hair = cv2.rotate(scaled_hair, cv2.ROTATE_180)

                    M = cv2.getRotationMatrix2D((rotated_hair.shape[1] // 2, rotated_hair.shape[0] // 2), -head_angle, 1)
                    rotated_hair = cv2.warpAffine(rotated_hair, M, (rotated_hair.shape[1], rotated_hair.shape[0]))
                    
                    pos_x = center_x - rotated_hair.shape[1] // 2
                    pos_y = center_y - rotated_hair.shape[0] // 2
                    
                    hair_rgb = rotated_hair[:, :, :3]
                    alpha = rotated_hair[:, :, 3]
                    hair_bgr = cv2.cvtColor(hair_rgb, cv2.COLOR_RGB2BGR)
                    self.overlay_image_alpha(frame, hair_bgr, (pos_x, pos_y), alpha)

    def adjust_hair_position(self, key):
        if key == ord('w'):
            self.y_offset -= 5
        elif key == ord('s'):
            self.y_offset += 5
        elif key == ord('a'):
            self.x_offset -= 5
        elif key == ord('d'):
            self.x_offset += 5
        elif key == ord('k'):
            self.scale_factor += 0.1
        elif key == ord('j'):
            self.scale_factor -= 0.1

    def change_style(self):
        styles = list(self.hair_styles.keys())
        current_idx = styles.index(self.current_style)
        self.current_style = styles[(current_idx + 1) % len(styles)]

        self.scale_factor = self.hair_scale_factors.get(self.current_style, 1.65)
        self.x_offset = self.hair_position_offsets.get(self.current_style, {}).get('x_offset', 0)
        self.y_offset = self.hair_position_offsets.get(self.current_style, {}).get('y_offset', -10)


# Tạo một instance của HairFilter để sử dụng chung
hair_filter_instance = HairFilter()

# View để xử lý yêu cầu điều chỉnh vị trí và kiểu tóc
@csrf_exempt
def adjust_hair_position(request):
    global hair_filter_instance
    if request.method == 'GET':
        action = request.GET.get('action', None)
        if action:
            # Gọi hàm adjust_hair_position hoặc change_style tương ứng với action
            if action == 'up':
                hair_filter_instance.adjust_hair_position(ord('w'))  # Tương ứng với phím 'w'
            elif action == 'down':
                hair_filter_instance.adjust_hair_position(ord('s'))  # Tương ứng với phím 's'
            elif action == 'left':
                hair_filter_instance.adjust_hair_position(ord('a'))  # Tương ứng với phím 'a'
            elif action == 'right':
                hair_filter_instance.adjust_hair_position(ord('d'))  # Tương ứng với phím 'd'
            elif action == 'change_style':
                hair_filter_instance.change_style()  # Đổi kiểu tóc

            return JsonResponse({'status': 'success', 'action': action})
        else:
            return JsonResponse({'status': 'error', 'message': 'No action provided'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# View để hiển thị video stream
def video_feed(request):
    def gen_frames():
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            if not ret:
                break

            try:
                hair_filter_instance.apply_hair(frame)
            except Exception as e:
                print(f"Error applying hair filter: {e}")

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        cap.release()

    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')










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
        model = tf.keras.models.load_model('ai_model/model1.keras')
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


