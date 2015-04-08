from django import template

from mysite.models import Wallpaper

register = template.Library()


class TemplateWallpaper(template.Node):
    def render(self, context):
        context['wallpaper'] = Wallpaper.get_random_wallpaper()
        return ''


@register.tag
def get_wallpaper(parser, token):
    return TemplateWallpaper()