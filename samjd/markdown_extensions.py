import markdown
from markdown.inlinepatterns import ImageInlineProcessor, IMAGE_LINK_RE
from .models import ProjectImage

class ProjectImageInlineProcessor(ImageInlineProcessor):
    def getLink(self, data, index):
        src, title, index, handled = super().getLink(data, index)
        if src.startswith("{{") and src.endswith("}}"):
            query_string = src.strip("{ }")
            image = query_string.split(".")[0]
            src = ProjectImage.objects.get(title=image).image.url
            if title is None:
                title = image

        return src, title, index, handled
    
    def getText(self, data, index):
        text, index, handled = super().getText(data, index)
        if text.startswith("{{") and text.endswith("}}"):
            query_string = text.strip("{ }")
            image = query_string.split(".")[0]
            text = ProjectImage.objects.get(title=image).alt_text
        return text, index, handled



class ProjectImageExtension(markdown.Extension):
    def extendMarkdown(self, md, *args, **kwargs):
        md.inlinePatterns.register(
            ProjectImageInlineProcessor(IMAGE_LINK_RE, md), "project_image_link", 155
        )
