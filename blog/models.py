from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from djgeojson.fields import PointField # https://django-geojson.readthedocs.io/en/latest/installation.html
from django.utils.safestring import mark_safe

class Blog(models.Model):
    baslik = models.CharField(max_length=255)
    icerik = RichTextUploadingField()  # ckeditor field'larından set ettik. Bu işlemden sonra makemigrations ve migrate ile veritabanına değişiklikleri yollamamız gerekmekte
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)
    yayin_mi = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    kategoriler = models.ManyToManyField(to='blog.Kategori', related_name='bloglar')  # Many To Many
    resim = models.ImageField(null=True,blank=True,default='defaults/default.png',upload_to='blog/')
    class Meta:  # Keyword'dur. Anlamamıza gerek yok, bilsek yeter
        verbose_name = 'Yazı'  # Tek bir Obje'nin panelde tanımı için
        verbose_name_plural = 'Yazılar'  # Objelerin tümünün paneldeki tanımı için

    def __str__(self):
        return self.baslik  # OOP'den gelmekte. Objelerimiz listelenirken neyi göstermek istiyoruz

    @property  # bu class'ın bir property'si olduğu için property decorator ile iaşretledik
    def kac_gun_once(self):
        fark = timezone.now() - self.eklenme_tarihi  # bugünün tarihi - eklenme tarihini değişkene atadık
        return fark.days()  # fark değişkeninin days prop'unu return ettik

    @property
    def kac_yorum_var(self):
        sayi = self.yorumlar.count()
        return sayi

    @property
    def detay_resim_getir(self):
        if self.resim:
            return mark_safe(f"<img src={self.resim.url} width=400 height=400></img>")
        return mark_safe(f"<h3>{self.baslik} adlı yazı resime sahip değil</h3>")
class Yorum(models.Model):
    blog = models.ForeignKey(to='blog.Blog', related_name='yorumlar', on_delete=models.CASCADE)
    yorum = models.TextField()
    yayin_mi = models.BooleanField(default=True)
    eklenme_tarihi = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        return f"{self.blog.baslik} - {self.yorum}"


class Kategori(models.Model):
    ad = models.CharField(max_length=100, verbose_name='Kategorinin Adı')
    yayin_mi = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.ad


class Mekan(models.Model):
    ad = models.CharField(max_length=255)
    lokasyon = PointField()

    def __str__(self):
        return self.ad
