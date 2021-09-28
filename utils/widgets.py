from django.conf import settings
from django_2gis_maps.widgets import DoubleGisMapsAddressWidget, DoubleGisMapsMultipleMarkersWidget


def get_static_url():
    if settings.DEBUG:
        return settings.STATIC_URL
    return settings.MINIO_STORAGE_STATIC_URL + '/'


class MinioDoubleGisMapsAddressWidget(DoubleGisMapsAddressWidget):
    class Media:
        css = {
            'all': (get_static_url() +
                    'django_2gis_maps/css/adminMap.css',)
        }
        js = (
            'https://code.jquery.com/jquery-latest.min.js',
            'https://maps.api.2gis.ru/2.0/loader.js?pkg=full&skin=dark',
            get_static_url() + 'django_2gis_maps/js/addMarkers.js',
            get_static_url() + 'django_2gis_maps/js/adminMap.js',
        )


class MinioDoubleGisMapsMultipleMarkersWidget(DoubleGisMapsMultipleMarkersWidget):
    class Media:
        css = {
            'all': (get_static_url() +
                    'django_2gis_maps/css/adminMapMultipleMarkers.css',)
        }
        js = (
            'https://code.jquery.com/jquery-latest.min.js',
            'https://maps.api.2gis.ru/2.0/loader.js?pkg=full&skin=dark',
            get_static_url() + 'django_2gis_maps/js/addMarkers.js',
            get_static_url() + 'django_2gis_maps/js/adminMapMultipleMarkers.js',
        )
