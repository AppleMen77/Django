from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserImage
from .forms import ImageUploadForm

class ImageEditorView(LoginRequiredMixin, View):
    template_name = 'image_editor/editor.html'

    def get(self, request):
        image_id = request.GET.get('image_id')
        image = None
        if image_id:
            try:
                image = UserImage.objects.get(id=image_id, user=request.user)
            except UserImage.DoesNotExist:
                pass
        form = ImageUploadForm()
        history = UserImage.objects.filter(user=request.user).order_by('-created_at')[:5]
        context = {
            'form': form,
            'image': image,
            'history': history,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'original_image' in request.FILES:
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.user = request.user
                image.save()
                # После сохранения перенаправляем на эту же страницу с новым image_id
                return redirect(f'{request.path}?image_id={image.id}')
        elif 'filter' in request.POST and 'image_id' in request.POST:
            image_id = request.POST.get('image_id')
            filter_name = request.POST.get('filter')
            try:
                image = UserImage.objects.get(id=image_id, user=request.user)
                image.apply_filter(filter_name)
            except UserImage.DoesNotExist:
                pass
            return redirect(f'{request.path}?image_id={image_id}')
        return redirect(request.path)