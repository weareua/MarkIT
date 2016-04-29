# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages

from groups.models import Group


def groups_list(request):

    groups = Group.objects.all()

    # order groups list
    order_by = request.GET.get('order_by', '')

    # ordering groups by title by default
    groups = groups.order_by('title')

    if order_by in ('title', 'leader', 'id'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    return render(request, 'groups_list.html', {'groups': groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


class GroupDeleteView(DeleteView):

    model = Group
    template_name = 'groups_confirm_delete.html'
    success_url = reverse_lazy('home')
    success_message = u"Група видалена успішно."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(GroupDeleteView, self).delete(
            request,
            *args,
            **kwargs)
