from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *


@api_view(['POST'])
def register(request):
    try:
        user = User(**request.data)
        user.set_password(request.data['password'])
        user.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print e

        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            user.access_token = request.META['HTTP_COOKIE'].split(';')[0].split('=')[1]
            user.save()
            go_to = '/issue/create_issue/'
            if 'next' in request.GET:
                go_to = request.GET['next']
            return redirect(go_to)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except KeyError as kerr:
        print kerr
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print e
        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET'])
def user_logout(request):
    try:
        logout(request)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print e
        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def create_issue(request):
    try:
        data = request.data
        data['created_by'] = request.user
        issue = Issue(**data)
        issue.save()
        return Response(status=status.HTTP_200_OK)
    except KeyError as kerr:
        print kerr
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print e
        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def assign_issue(request):
    try:
        created_by = request.data['created_by']
        assigned_to = User.objects.get(id=request.data['assigned_to'])
        issues = Issue.objects.filter(created_by=created_by, assigned_to=None)
        with transaction.atomic():
            for issue in issues:
                issue.assigned_to = assigned_to
                issue.save()
        return Response(status=status.HTTP_200_OK)
    except KeyError as kerr:
        print kerr
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print e
        return Response(status=status.HTTP_400_BAD_REQUEST)


def send_automated_email():
    subject = 'Issues assigned to you'
    assigned_to_ids = Issue.objects.exclude(Q(assigned_to=None) or Q(status='Closed')).values_list('assigned_to',
                                                                                                   flat=True).distinct()
    for a_id in assigned_to_ids:
        issues = Issue.objects.filter(assigned_to=a_id).values('title', 'description', 'status',
                                                               'created_by__first_name', 'created_by__last_name',
                                                               'created_by__email')

        message = 'You have been assigned the following Issues\n\n'

        records = ''
        for issue in issues:
            records += 'Title:- ' + issue['title'] + '\n' + \
                       'Description:- ' + issue['description'] + '\n' + \
                       'Status:- ' + issue['status'] + '\n' + \
                       'Created By:- ' + issue['created_by__first_name'] + ' ' + issue['created_by__last_name'] + \
                       '\n\n'

        message += records

        email = issues[0]['created_by__email']
        send_email(subject, message, email)

    return Response(status=status.HTTP_200_OK)
