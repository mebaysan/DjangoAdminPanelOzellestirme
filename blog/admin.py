from django.contrib import admin
from blog.models import Blog, Yorum, Kategori, Mekan
from django.utils import timezone
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filter import DateTimeRangeFilter  # https://github.com/silentsokolov/django-admin-rangefilter
from leaflet.admin import LeafletGeoAdmin  # https://django-leaflet.readthedocs.io/en/latest/installation.html
from import_export.admin import ImportExportModelAdmin
from blog.resources import YorumResource # https://django-import-export.readthedocs.io/en/latest/index.html


class YorumInline(admin.TabularInline):
    model = Yorum  # hangi model üzerinde çalışacağız
    fields = ('yorum', 'yayin_mi')  # hangi field'lar ile işlem yapacağız
    extra = 1  # extra kaç adet form field olsun
    classes = ('collapse',)  # Dropdown yapısı için class ekledik


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'baslik', 'eklenme_tarihi', 'guncellenme_tarihi', 'yayin_mi',
        'kac_gun_once', 'kac_yorum_var')  # Liste sayfasında hangi field'lar listelensin
    list_filter = ('yayin_mi', (
        'eklenme_tarihi', DateTimeRangeFilter),)  # istediğimiz field'a göre sağ tarafta bir süzgeç çıkar (yayin mı vb.)
    ordering = ('baslik',
                '-guncellenme_tarihi')  # verilerimizi hangi field'lara göre sıralayacağız. 'baslik' -> A'dan Z'ye (küçükten büyüğe), '-baslik' -> Z'den A'ya (büyükten küçüğe)
    search_fields = (
        'baslik',)  # istediğimiz field'lara göre search bar'da arama yapabiliriz ve bu kelimeler hangi field'lar içerisinde aranacak
    prepopulated_fields = {
        'slug': ('baslik',)}  # birbiri ile bağıntılı olan field'lar kullanılır.  {'hangi_field',('neye_ile_bagli',)}
    list_per_page = 50  # sayfa başına kaç adet veri göstermek istiyoruz
    actions = ('yayina_al',)
    date_hierarchy = 'guncellenme_tarihi'
    # fields=(('baslik','slug'),'icerik','yayin_mi') # tuple içerisindeki her eleman 1 satıra denk gelir. eleman olarak tuple verirsek ve içerisine istediğimiz fieldları geçersek tek satırda gözükecektir
    fieldsets = (
        (None, {  # None -> Field kümemizin başlığı
            'fields': (('baslik', 'slug'), 'icerik'),  # bu kümede hangi field'lar gözükecek
            'description': 'Yazı için genel ayarlar'  # bu kümenin açıklaması
        }),  # 2. kümemizi verirken tekrar tuple olarak vermeliyiz
        ('Opsiyonel Ayarlar', {
            'fields': ('yayin_mi', 'kategoriler'),
            # sonradan eklediğimiz fieldları field kümelerimize eklemeyi unutmamalıyız
            'description': 'Opsyionel Ayarlar için bu kümeyi kullanabilirsiniz',
            'classes': ('collapse',)  # Dropdown yapısı
        })
    )
    filter_horizontal = ('kategoriler',)  # yatay many to many filtreleme
    inlines = (YorumInline,)  # Hangi class'ı inline olarak ekleyeceğiz (birden çok olabilir)

    def kac_gun_once(self, blog):  # parametre olarak blog objesi alacak
        fark = timezone.now() - blog.eklenme_tarihi  # parametre olarak aldığı blogun eklenme tarihini çıakrtacak
        return fark.days

    def yayina_al(self, request, queryset):
        count = queryset.update(yayin_mi=True)
        self.message_user(request, f"{count} adet yazı yayına alındı")

    yayina_al.short_description = 'İşaretlenen Yazıları Yayına Al'


class YorumAdmin(ImportExportModelAdmin):
    list_display = ('__str__', 'eklenme_tarihi', 'yayin_mi')
    list_per_page = 50
    list_editable = ('yayin_mi',)
    list_filter = (
        ('blog', RelatedDropdownFilter),  # https://github.com/mrts/django-admin-list-filter-dropdown
    )
    resource_class = YorumResource
    raw_id_fields = ('blog',)

    def has_delete_permission(self, request, obj=None): # kendi class'ımızı override ettik ve silinebilme özelliğini kapattık
        return False

admin.site.register(Blog,
                    BlogAdmin)  # Model Admin class'ı oluşturduğumuzda, bunu admin app'e register ederken ilgili model ile veriyoruz ve Django otomatik bind ediyor

admin.site.register(Yorum, YorumAdmin)

admin.site.register(Kategori)
admin.site.register(Mekan, LeafletGeoAdmin)
