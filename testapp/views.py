from django.shortcuts import render
from django.views.generic import View
from pyparsing import original_text_for
from .models import Employee
from django.http import HttpResponse
from django.core.serializers import serialize
from .mixins import HttpResponseMixin
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import is_json

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeDetailCBV(HttpResponseMixin,View):
    def get(self,request,*args,**kwargs):
        # emp = Employee.objects.get(id = 4)
        # emp_data = {
        #     'eno' : emp.eno,
        #     'ename' : emp.ename,
        #     'esal' : emp.esal,
        #     'eaddr' : emp.eaddr
        # }
        # json_data = json.dumps(emp_data)

        try:
            emp = Employee.objects.get(id = 2)
        except Employee.DoesNotExist:
            return HttpResponse(json.dumps({'msg' : "The required resource not found"}), content_type = 'application/json',status = 404)

        json_data = serialize('json',[emp],fields=('eno','ename','eaddr'))
        return HttpResponse(self.json_response_data(json_data), content_type = 'application/json',status = 200)

    def put(self,request,*args,**kwargs):
        emp_body = json.loads(request.body)
        try:
            emp = Employee.objects.get(id = emp_body['id'])
        except Employee.DoesNotExist:
            return HttpResponse(json.dumps({'msg': "user didn't exists"}),
            content_type = 'application/json',status = 404)
        else:
            new_data = emp_body['data']

            original_data = {
                'eno' : emp.eno,
                'ename' : emp.ename,
                'esal' : emp.esal,
                'eaddr' : emp.eaddr
            }
            
            for keys,value in new_data.items():
                original_data[keys] = value

            emp.eno = original_data['eno']
            emp.ename = original_data['ename']
            emp.esal = original_data['esal']
            emp.eaddr = original_data['eaddr']
            emp.save()            
          
            return HttpResponse(json.dumps({'msg': "data updated successfully"}),
            content_type = 'application/json',status = 200)

    def delete(self,request,*args,**kwargs):
        emp_body = json.loads(request.body)
        try:
            emp = Employee.objects.get(id = emp_body['id'])
            emp.delete()
        except Employee.DoesNotExist:
            return HttpResponse(json.dumps({'msg': "user didn't exists"}),
            content_type = 'application/json',status = 404)
            
        return HttpResponse(json.dumps({'msg': "data delete successfully"}),
        content_type = 'application/json',status = 200)

        

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeListCBV(HttpResponseMixin,View):
    def get(self, request,*args,**kwargs):
        all_emp = Employee.objects.all()
        json_data_all = serialize('json',all_emp,fields=('eno','ename','eaddr'))
        return HttpResponse(self.json_response_data(json_data_all), content_type = 'application/json')

    def post(self, request, *args, **kwargs):
        if not is_json(request.body):
            return HttpResponse(json.dumps({'msg': 'please send valid data'}),content_type = 'application/json',status = 400)
        emp_dict = json.loads(request.body)
        emp_data = Employee(eno= emp_dict['eno'], ename = emp_dict['ename'], esal = emp_dict['esal'], eaddr = emp_dict['eaddr'] )
        emp_data.save()
        return HttpResponse(json.dumps({'msg': 'added successfully'}),
            content_type = 'application/json',status = 200)
        
