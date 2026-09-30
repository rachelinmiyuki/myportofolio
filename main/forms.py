from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "project_type",
            "thumbnail",
            "tag1",
            "tag2",
            "tag3",
            "tag4",
            "detail_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "project_type": "Tipe Proyek",
            "thumbnail": "URL Gambar Proyek",
            "tag1": "Teknologi 1 yang Digunakan",
            "tag2": "Teknologi 2 yang Digunakan",
            "tag3": "Teknologi 3 yang Digunakan",
            "tag4": "Teknologi 4 yang Digunakan",
            "detail_url": "URL Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "project_type": TextInput(
                attrs={
                    "placeholder": "Tipe Proyekmu",
                    "maxlength": 255,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "tag1": TextInput(
                attrs={
                    "placeholder": "Django",
                }
            ),
            "tag2": TextInput(
                attrs={
                    "placeholder": "Python",
                }
            ),
            "tag3": TextInput(
                attrs={
                    "placeholder": "HTML",
                }
            ),
            "tag4": TextInput(
                attrs={
                    "placeholder": "CSS",
                }
            ),
            
                    
            "detail_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()
    
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Tipe Pengalaman",
            "thumbnail": "URL Gambar Pengalaman",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Staff Public Relations - Open House 2026",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Pengalamanmu",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "Tipe Pengalamanmu",
                    "maxlength": 255,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

