from django.contrib.admin import ModelAdmin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME


class NoObjNeededMixin:
    def changelist_view(self, request, extra_context=None):
        if (
            request
            and request.POST
            and request.POST.get("action", None) == "calculate_all_statistics"
        ):
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                post.update({ACTION_CHECKBOX_NAME: "No Changelist"})
                request._set_post(post)
        return ModelAdmin.changelist_view(request, extra_context)

    #
    # class Meta:
    #     abstract = True
