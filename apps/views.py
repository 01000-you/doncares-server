# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Driver
from django.db.models import Q

from .forms import DriverForm
# from .forms import DriverSearchForm
from .models import Customer
from .forms import CustomerForm
from .models import KakaoUser
from .forms import KakaoUserForm

from django.views.decorators.csrf import csrf_exempt # 보안 이슈를 피하기 위한 csrf_exempt
from rest_framework.parsers import JSONParser
import json

from django.http import JsonResponse
import httplib2
import requests

rest_api_key = "112afaa24e7a12c43eeb42a4e57e72f0"

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer_detail.html', {'customer': customer})

@csrf_exempt
def customer_validate(request):
    if request.method == 'POST':
        try:
            body_data = json.loads(request.body)
            app_user_id = body_data['userRequest']['user']['properties']['app_user_id']
        except (KeyError, TypeError):
            app_user_id = None

        if app_user_id:
            # app_user_id가 있는 경우에는 처리 결과를 담은 JSON 응답을 반환합니다.
            response_data = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "textCard": {
                                "text": "고객님의 회원 정보가 확인되었습니다.\n 아래 버튼을 통해 고객 등록을 진행해주세요",
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": "고객 정보 입력하기",
                                        "blockId": "64c1f2927b110851437c0b06"
                                    }
                                ]
                            }
                        }
                    ]
                },
            }
            return JsonResponse(response_data)

        # app_user_id가 없는 경우에는 다른 형식의 템플릿을 담은 JSON 응답을 반환합니다.
        other_template_data = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "textCard": {
                            "text": "고객님의 가입 정보가 없습니다.\n아래 버튼을 통해 인증 후 다시 '고객 등록'을 이용해주시기 바랍니다.",
                            "buttons": [
                                {
                                    "action": "block",
                                    "label": "인증하러 가기",
                                    "blockId": "64c6163ac78ec6198958bf85"
                                }
                            ]
                        }
                    }
                ]
            },
        }
        return JsonResponse(other_template_data)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def customer_create(request):
    if request.method == 'POST':
        # print(request.content_type)
        if request.content_type == 'application/json':
            body_data = json.loads(request.body)
            data = body_data.get('action','fail').get('params','fail')
            app_user_id = body_data.get('userRequest','fail').get('user', 'fail').get('properties', 'fail').get('app_user_id','fail')
            data['app_user_id'] = app_user_id
        else :
            data = request.POST

        form = CustomerForm(data)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'customer_create.html', {'form': form})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'customer_update.html', {'form': form, 'customer': customer})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    
    return render(request, 'customer_delete.html', {'customer': customer})

def customer_search(request):
    query = request.GET.get('q')
    if query:
        customers = Customer.objects.filter(
            Q(app_user_id__icontains=query) |
            Q(name__icontains=query) |
            Q(region__icontains=query) |
            Q(target__icontains=query) |
            Q(period__icontains=query)
        )
    else:
        customers = Customer.objects.all()

    return render(request, 'customer_search.html', {'customers': customers, 'query': query})

def kakao_user_list(request):
    users = KakaoUser.objects.all()
    return render(request, 'kakao_user_list.html', {'users': users})

def kakao_user_detail(request, pk):
    user = get_object_or_404(KakaoUser, pk=pk)
    return render(request, 'kakao_user_detail.html', {'user': user})

@csrf_exempt
def kakao_user_create(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            
            body_data = json.loads(request.body)
            params = body_data.get('action', {}).get('params', {})
            customer_proflie = params.get('customer_proflie', {})
            json_customer_proflie = json.loads(customer_proflie)
            otp_url = json_customer_proflie.get('otp', '')
            url = f"{otp_url}?rest_api_key={rest_api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
            else:
                return JsonResponse({"status": "failure", "message": "Failed to create Kakao user."})
        else:
            data = request.POST

        form = KakaoUserForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'errors': form.errors})
    else:
        form = KakaoUserForm()

    return render(request, 'kakao_user_create.html', {'form': form})

def kakao_user_update(request, pk):
    user = get_object_or_404(KakaoUser, pk=pk)
    if request.method == 'POST':
        form = KakaoUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = KakaoUserForm(instance=user)
        return render(request, 'kakao_user_update_form.html', {'form': form})

def kakao_user_delete(request, pk):
    user = get_object_or_404(KakaoUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('kakao_user_list')
    return render(request, 'kakao_user_delete.html', {'user': user})

def kakao_user_search(request):
    search_query = request.GET.get('search_query')
    search_results = []

    if search_query:
        # 검색어를 사용하여 KakaoUser 모델을 필터링합니다.
        search_results = KakaoUser.objects.filter(
            nickname__icontains=search_query
        )  # 닉네임에 검색어가 포함된 경우를 찾습니다.

    context = {'search_results': search_results}
    return render(request, 'kakao_user_search.html', context)

def driver_list(request):
    search_query = request.GET.get('search_query')
    if search_query:
        drivers = Driver.objects.filter(
            Q(name__icontains=search_query) |
            Q(region__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(app_user_id__icontains=search_query)
        )
    else:
        drivers = Driver.objects.all()
    return render(request, 'driver_list.html', {'drivers': drivers})

def driver_detail(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    return render(request, 'driver_detail.html', {'driver': driver})

@csrf_exempt
def driver_create(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                body_data = json.loads(request.body)
                data = body_data['action']['params']
                app_user_id = body_data['userRequest']['user']['properties']['app_user_id']
                data['app_user_id'] = app_user_id

            except (json.JSONDecodeError, KeyError):
                return JsonResponse({'status': 'failure', 'errors': 'Invalid JSON data.'}, status=400)
        else:
            data = request.POST

        form = DriverForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'errors': form.errors}, status=400)
    else:
        form = DriverForm()
    
    return render(request, 'driver_create.html', {'form': form})

def driver_update(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = DriverForm(instance=driver)
        return render(request, 'driver_update.html', {'form': form})

def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')
    return render(request, 'driver_delete.html', {'driver': driver})

# @csrf_exempt
# def driver_create(request):
#     if request.method == 'POST':
#         # print(request.content_type)
#         if request.content_type == 'application/json':
#             # JSON 데이터를 파싱하여 처리
#             # data = JSONParser().parse(request)
#             data = json.loads(request.body)
#             print('body: ',data)
#             data = data.get('action','fail').get('params','fail')
#             print('params: ',data)
#         else:
#             # 폼 데이터를 사용하여 처리
#             data = request.POST
#         # form = DriverForm(request.POST)
#         form = DriverForm(data)
        
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'status': 'success'})
#         else:
#             print(form.errors)
#             return JsonResponse({'status': 'failure', 'errors': form.errors})
#     else:
#         form = DriverForm()
    
#     return render(request, 'driver_create.html', {'form': form})
    
def driver_search(request):
    query = request.GET.get('q')

    if query:
        drivers = Driver.objects.filter(
            Q(name__icontains=query) |
            Q(region__icontains=query) |
            Q(phone_number__icontains=query)
                )
    else:
        drivers = Driver.objects.all()

    return render(request, 'driver_list.html', {'drivers': drivers, 'query': query})

@csrf_exempt
def driver_validate(request):
    if request.method == 'POST':
        try:
            body_data = json.loads(request.body)
            app_user_id = body_data['userRequest']['user']['properties']['app_user_id']
        except (KeyError, TypeError):
            app_user_id = None

        if app_user_id:
            # app_user_id가 있는 경우에는 처리 결과를 담은 JSON 응답을 반환합니다.
            response_data = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "textCard": {
                                "text": "고객님의 회원 정보가 확인되었습니다.\n 아래 버튼을 통해 기사 등록을 진행해주세요",
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": "기사 정보 입력하기",
                                        "blockId": "64bf7bd07b110851437bb7f9"
                                    }
                                ]
                            }
                        }
                    ]
                },
            }
            return JsonResponse(response_data)

        # app_user_id가 없는 경우에는 다른 형식의 템플릿을 담은 JSON 응답을 반환합니다.
        other_template_data = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "textCard": {
                            "text": "고객님의 가입 정보가 없습니다.\n아래 버튼을 통해 인증 후 다시 '기사 등록'을 이용해주시기 바랍니다.",
                            "buttons": [
                                {
                                    "action": "block",
                                    "label": "인증하러 가기",
                                    "blockId": "64c6163ac78ec6198958bf85"
                                }
                            ]
                        }
                    }
                ]
            },
        }
        return JsonResponse(other_template_data)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def skill_view(request):
    if request.method == 'POST':
        # 요청에 필요한 처리를 수행하고, 필요한 데이터를 가져오는 로직을 구현합니다.
        version = "2.0"
        template = {
            # 템플릿 정보를 정의합니다.
            "outputs": [
                {
                    "textCard": {
                        "text": "챗봇 관리자센터에 오신 것을 환영합니다 🙂\n\n챗봇 관리자센터로 챗봇을 제작해 보세요. \n카카오톡 채널과 연결하여, 이용자에게 챗봇 서비스를 제공할 수 있습니다.",
                        "buttons": [
                            {
                            "action": "block",
                            "label": "예약하기",
                            "blockId": "64ba7f5bb340b35ea870be62"
                            },
                            {
                            "action": "webLink",
                            "label": "챗봇 만들러 가기",
                            "webLinkUrl": "https://chatbot.kakao.com/"
                            }
                        ]
                    }
                }
            ]
        }
        context = {
            # 컨텍스트 정보를 정의합니다.
        }
        data = {
            # 데이터 정보를 정의합니다.
        }


        response_data = {
            "version": version,
            "template": template,
            # "context": context,
            # "data": data,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
