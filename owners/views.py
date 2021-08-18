import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from owners.models import Owner, Dog


# Create your views here.


class OwnerRegister(View):
    def post(self, request):
        data = json.loads(request.body)
        owner = Owner.objects.create(
            name=data["name"],
            email=data["email"],
            age=data["age"]
        )

        return JsonResponse({"result": data}, status=201)


class DogRegister(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            owner = Owner.objects.get(name=data["owner_name"])
        except:
            return HttpResponseBadRequest(
                "No matching owner name, please check your owner name again!"
            )

        dog = Dog.objects.create(
            name=data['name'],
            age=data['age'],
            owner=owner
        )

        return JsonResponse({"result": data}, status=201)

class ViewOwner(View):
    def get(self, request):

        owners = Owner.objects.all()

        return_json = []
        dog_list = []

        for owner in owners:
            owner_dog = owner.dog_set.all()

            for dog in owner_dog:
                dog_list.append({
                    "dog_name": dog.name,
                    "dog_age": dog.age,
                })

            return_json.append({
                "owner_name": owner.name,
                "email": owner.email,
                "age": owner.age,
                "dog_list": dog_list,
            })

        return JsonResponse({'owner_list': return_json}, status=201)


class ViewDog(View):
    def get(self, request):
        dogs = Dog.objects.all()
        return_json = []

        for dog in dogs:
            return_json.append(
                {
                    "name": dog.name,
                    "age": dog.age,
                    "owner_id": dog.owner_id
                }
            )

        return JsonResponse({'dog_list': return_json}, status=201)


