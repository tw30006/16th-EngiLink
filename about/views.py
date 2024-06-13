from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Payment
import json
import hashlib
import hmac
import base64
import time
import uuid
import requests

def generate_signature(channel_secret, uri, request_body, nonce):
    raw_signature = f'{channel_secret}{uri}{request_body}{nonce}'
    signature = hmac.new(
        channel_secret.encode('utf-8'),
        raw_signature.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')

def create_line_pay_request(amount, currency, order_id):
    api_url = "/v3/payments/request"
    request_body_dict = {
        'amount': int(amount),
        'currency': currency,
        'orderId': order_id,
        'packages': [
            {
                'id': 'package-1',
                'amount': int(amount),
                'name': 'Donation',
                'products': [
                    {
                        'name': 'Donation',
                        'quantity': 1,
                        'price': int(amount),
                        'imageUrl': 'https://example.com/donation.jpg'
                    }
                ]
            }
        ],
        'redirectUrls': {
            'confirmUrl': settings.ONLINE_URL + "about/",
            'cancelUrl': settings.ONLINE_URL + "/linepay/cancel/"
        }
    }
    request_body = json.dumps(request_body_dict)
    nonce = str(int(time.time() * 1000))
    signature = generate_signature(settings.LINE_PAY_CHANNEL_SECRET, api_url, request_body, nonce)

    headers = {
        'Content-Type': 'application/json',
        'X-LINE-ChannelId': settings.LINE_PAY_CHANNEL_ID,
        'X-LINE-Authorization-Nonce': nonce,
        'X-LINE-Authorization': signature
    }

    response = requests.post(
        f"{settings.LINE_PAY_API_URL}{api_url}",
        headers=headers,
        data=request_body
    )

    return response.json()

@method_decorator(csrf_exempt, name='dispatch')
class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about/about.html')

    def post(self, request, *args, **kwargs):
        amount = request.POST.get('amount')
        order_id = str(uuid.uuid4())

        payment = Payment.objects.create(
            order_id=order_id,
            amount=amount,
            currency='TWD',
            status='pending'
        )

        response = create_line_pay_request(amount, 'TWD', order_id)

        if response['returnCode'] == '0000':
            payment_url = response['info']['paymentUrl']['web']
            payment.transaction_id = response['info']['transactionId']
            payment.status = 'success'
            payment.save()
            messages.success(request, "感謝您的贊助")

            return redirect(payment_url)
        else:
            payment.status = 'failed'
            payment.save()
            message = {
                'title': 'Payment Failed',
                'text': response['returnMessage'],
                'icon': 'error'
            }
            return render(request, 'about/about.html', {'message': message})

@method_decorator(csrf_exempt, name='dispatch')
class LinePayRequestView(View):
    def post(self, request, *args, **kwargs):
        uri = '/v2/payments/request'
        nonce = str(int(time.time() * 1000))
        request_body = json.dumps({
            "amount": 1000,
            "currency": "TWD",
            "orderId": "12345",
            "packages": [
                {
                    "id": "package-12345",
                    "amount": 1000,
                    "name": "Product Package",
                    "products": [
                        {
                            "id": "product-123",
                            "name": "Product Name",
                            "quantity": 1,
                            "price": 1000
                        }
                    ]
                }
            ],
            "redirectUrls": {
                "confirmUrl": f"{settings.ONLINE_URL}about/",
                "cancelUrl": f"{settings.ONLINE_URL}/linepay/cancel/"
            }
        }, separators=(',', ':'))

        signature = generate_signature(settings.LINE_PAY_CHANNEL_SECRET, uri, request_body, nonce)

        headers = {
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': settings.LINE_PAY_CHANNEL_ID,
            'X-LINE-Authorization-Nonce': nonce,
            'X-LINE-Authorization': signature
        }

        response = requests.post('https://api-pay.line.me/v2/payments/request', headers=headers, data=request_body)
        response_data = response.json()

        if response_data['returnCode'] == '0000':
            payment_url = response_data['info']['paymentUrl']['web']
            return redirect(payment_url)
        else:
            return JsonResponse({'error': response_data['returnMessage']})

@method_decorator(csrf_exempt, name='dispatch')
class LinePayCallbackView(View):
    def post(self, request, *args, **kwargs):
        transaction_id = request.POST.get('transactionId')
        order_id = request.POST.get('orderId')

        if transaction_id and order_id:
            try:
                payment = Payment.objects.get(order_id=order_id)
                payment.transaction_id = transaction_id
                payment.status = 'completed'
                payment.save()

                message = {
                    'title': 'Payment Successful',
                    'text': '感謝您的贊助',
                    'icon': 'success'
                }
                return render(request, 'about/about.html', {'message': message})
            
            except Payment.DoesNotExist:
                message = {
                    'title': 'Payment Failed',
                    'text': '無效的訂單ID',
                    'icon': 'error'
                }
                return render(request, 'about/about.html', {'message': message})
        else:
            return HttpResponse("Invalid callback parameters", status=400)
