import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from bigcommerce.api import BigcommerceApi
from django.views import View
from .models import *
from django.views.decorators.clickjacking import xframe_options_exempt


os.environ['APP_CLIENT_SECRET'] = 'oam9jfaj4n7olb6gnxetiza5jozt83h'

# api = BigcommerceApi(
#     client_id='dfgb1ixry16pqf83tvdwaamvev8d4a7',
#     store_hash='d2mevog548',
#     access_token='tqmm1s7dvi36mrmqie7yihagrj24owp')
#


class Display(View):

    template = "display.html"

    @xframe_options_exempt
    def get(self, request):
        # customer = api.Customers.all()
        # login_token = bigcommerce.customer_login_token.create(api, customer.id)
        # print('%s/login/token/%s' % ('http://localhost:8000', login_token))
        print("display===>", request)
        customer = "customer details"
        return render(request, self.template, locals())

    def post(self, request):
        pass


class AuthCallback(View):

    template = "callback.html"

    def get(self, request):
        code = request.GET['code']
        print("code=====> ", code)
        context = request.GET['context']
        print("context=====> ", context)
        scope = request.GET['scope']
        print("scope=====> ", scope)
        store_hash = context.split('/')[1]
        print("store has=====> ", store_hash)
        redirect = settings.APP_URL + 'bigcommerce/callback'
        print("redirect=====> ", redirect)
        client = BigcommerceApi(client_id=settings.APP_CLIENT_ID, store_hash=store_hash)
        token = client.oauth_fetch_token(settings.APP_CLIENT_SECRET, code, context, scope, redirect)
        bc_user_id = token['user']['id']
        email = token['user']['email']
        print("email===>", email)
        access_token = token['access_token']
        print("access_tocken====>", access_token)

        store = Store.objects.filter(store_hash=store_hash).first()
        if store is None:
            store = Store.objects.create(
                store_hash=store_hash,
                access_token=access_token,
                scope=scope,
            )
            print("============>>Create new store")
        else:
            Store.objects.update(
                access_token=access_token,
                scope=scope,
            )
            print("============>>Update new store")

        user = User.objects.filter(bc_id=bc_user_id).first()
        if user is None:
            user = User.objects.create(
                bc_id=bc_user_id,
                email=email,
            )
            print("============>>Create new user")
        elif user.email != email:
            User.update(
                email=email,
            )
            print("============>>update new user")

        storeuser = StoreUser.objects.filter(
            user_id=user.id,
            store_id=store.id,
        ).first()

        if not storeuser:
            storeuser = StoreUser.objects.create(
                store_id=store,
                user_id=user,
                admin=True,
            )
            print("============>>Create new storeuser")
        else:
            StoreUser.objects.update(admin=True)
            print("============>>Update new storeuser")

        print("====>Auth redirect APP_URL", settings.APP_URL)
        return HttpResponseRedirect(settings.APP_URL)


class Load(View):

    template = "callback.html"

    def get(self, request):
        payload = request.GET['signed_payload']
        print("payload========>", payload)
        user_data = BigcommerceApi.oauth_verify_payload(payload, settings.APP_CLIENT_SECRET)
        print("userdata======>", user_data)
        if user_data is False:
            return "Payload verification failed!"

        bc_user_id = user_data['user']['id']
        print("bc id=========>", bc_user_id)
        email = user_data['user']['email']
        print("email =========>", email)
        store_hash = user_data['store_hash']
        print("store has=========>", store_hash)

        store = Store.objects.filter(store_hash=store_hash).first()
        if store is None:
            return "Store not found!"

        user = User.objects.filter(bc_id=bc_user_id).first()
        if user is None:
            user = User.objects.create(
                bc_id=bc_user_id,
                email=email,
            )
            print("============>>Create new user")

        storeuser = StoreUser.objects.filter(user_id=user.id, store_id=store.id).first()
        if storeuser is None:
            storeuser = StoreUser.objects.create(
                store_id=store,
                user_id=user,
            )
            print("============>>Create new userstore")

        print("====>Load redirect APP_URL", settings.APP_URL)
        return HttpResponseRedirect(settings.APP_URL)
