from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponse, JsonResponse
from . models import *
import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# Create your views here.



def home(request):
    return render(request, 'home.html')


@login_required(login_url='/login_page')
def add_form_home(request):
    return render(request, 'add_form_home.html')


@login_required(login_url='/login_page')
def add_form_parent(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        banner = request.FILES.get('banner')
        # print(banner)
        if banner is not None:
            form_parent_obj = FormParent(title=title, description=description, builder = request.user.profile, banner_img = banner)
        else:
            form_parent_obj = FormParent(title=title, description=description, builder = request.user.profile)
        # form_parent_obj = FormParent(title=title, description=description, builder = request.user.profile)
        form_parent_obj.save()
        
        return redirect('/add_form_fields/' + str(form_parent_obj.pk))


@login_required(login_url='/login_page')
def add_form_fields(request, pk):
    form_parent_obj =get_object_or_404(FormParent,id=pk)
    form_designs = FormDesign.objects.filter(form_parent=form_parent_obj)
    formobjs = FormObject.objects.filter(form_parent=form_parent_obj)
    if request.method == 'POST':
        label_name = request.POST.get('label_name', '')
        field_type = request.POST.get('field_type', '')
        
        # print(label_name)
        # print(field_type)
        if field_type == 'CF':
            form_design_obj = FormDesign(
                label=label_name,
                character_field = True,
                form_parent=form_parent_obj

            )
            form_design_obj.save()
        elif field_type == 'TF':
            form_design_obj = FormDesign(
                label=label_name,
                big_text_field = True,
                form_parent=form_parent_obj
               
            )
            form_design_obj.save()
        elif field_type == 'IF':
            form_design_obj = FormDesign(
                label=label_name,
                integer_field = True,
                form_parent=form_parent_obj
              
            )
            form_design_obj.save()
        elif field_type == 'FF':
            form_design_obj = FormDesign(
                label=label_name,
                file_field = True,
                form_parent=form_parent_obj
             

            )
            form_design_obj.save()
        elif field_type == 'MF':
            options_value = request.POST.get('options_value', '')
            
            form_design_obj = FormDesign(
                label=label_name,
                mcq_field = True,
                form_parent=form_parent_obj
             

            )
            form_design_obj.save()
            for i in options_value.split(','):
                choice_obj = Choice(name=i, mcq_parent= form_design_obj)
                choice_obj.save()

        
    context = {
            'form_parent':form_parent_obj,
            'form_designs':form_designs,
            'formobjs':formobjs

        }

    return render(request, 'add_form_fields.html', context)



@login_required(login_url='/login_page')
def delete_form_field(request, pk):
    form_field = get_object_or_404(FormDesign, pk=pk)
    form_parent = form_field.form_parent
    # print(form_field)

    if form_parent.builder == request.user.profile:
        form_field.delete()

    return redirect('/add_form_fields/' + str(form_parent.pk))


@login_required(login_url='/login_page')
def form_view(request, unique_id):
    form_parent_obj = get_object_or_404(FormParent, unique_id=unique_id)
    form_designs = FormDesign.objects.filter(form_parent=form_parent_obj)
    formobj = FormObject.objects.filter(form_parent=form_parent_obj, applicant = request.user.profile)
    context ={
        'form_parent':form_parent_obj,
        'form_designs':form_designs,
        'formobj':formobj
    }
    
    
    return render(request, 'user_view/form_view.html', context)

@login_required(login_url='/login_page')
def form_submit(request, unique_id):
    form_parent_obj = get_object_or_404(FormParent, unique_id=unique_id)
    form_designs = FormDesign.objects.filter(form_parent=form_parent_obj)
    profile = get_object_or_404(Profile, user = request.user)
    form_obj = FormObject(
        form_parent = form_parent_obj,
        applicant = profile

    )
    form_obj.save()
    # print("kk")

    if request.method == 'POST':
        for field in form_designs:
            if field.character_field:
                # print(field.pk)
                form_char_obj = FormCharacterField(
                    field_data = request.POST.get(str(field.pk)),
                    form_object = form_obj,
                    label_name = request.POST.get('char' + str(field.pk))  
                )
                form_char_obj.save()
            elif field.big_text_field:
                form_txt_field = FormBigTextField(
                    field_data = request.POST.get(str(field.pk)),
                    form_object = form_obj, 
                    label_name = request.POST.get('txt' + str(field.pk))

                )
                form_txt_field.save()
            elif field.integer_field:
                form_int_field = FormIntegerField(
                    field_data = request.POST.get(str(field.pk)),
                    form_object = form_obj,
                    label_name = request.POST.get('int' + str(field.pk)) 

                )
                form_int_field.save()
            elif field.file_field:

                form_file_field = FormFileField(
                    field_data = request.FILES[str(field.pk)],
                    form_object = form_obj, 
                    label_name = request.POST.get('file' + str(field.pk))

                )
                form_file_field.save()
            elif field.mcq_field:
                choices = field.choice_set.all()
                checked = request.POST.get('flexRadioDefault' + str(field.pk))
                # print(checked)
                form_mcq_field = MCQField(
                   field_data = checked,
                   form_object = form_obj,
                   label_name = request.POST.get('mcq' + str(field.pk)),
                   form_design = field
                   
                )
                # form_mcq_field.form_design.add(field)
                form_mcq_field.save()
        return redirect('/form_view/' + str(unique_id))


@login_required(login_url='/login_page')
def responses(request, pk):
    form_parent = FormParent.objects.filter(builder = request.user.profile, pk =pk)
    data_dict ={}
    # print(form_parent)
    if form_parent:
        

        form_designs = FormDesign.objects.filter(form_parent = form_parent[0])
        formobjs = FormObject.objects.filter(form_parent = form_parent[0])
        
        for obj in formobjs:
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj] ={}
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['chars'] =[FormCharacterField.objects.filter(form_object = obj)]
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['txts'] =[ FormBigTextField.objects.filter(form_object = obj)]
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['ints'] =[ FormIntegerField.objects.filter(form_object = obj)]
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['files'] =[ FormFileField.objects.filter(form_object = obj)]
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['mcq'] =[ MCQField.objects.filter(form_object = obj)]
            
         

                
        mcq_design = FormDesign.objects.filter(form_parent = form_parent[0], mcq_field= True)[0]


        # print(data_dict)
        context={
            'data_dict':data_dict,
            'form_parent':form_parent,
            'mcq_design':mcq_design
        }
    else:
        # print("no form")
        context = {
            'data_dict':data_dict,
            
        }
        return redirect('/forms')

    return render(request,'responses.html', context)


@login_required(login_url='/login_page')
def accept_responses_toggle(request, pk):
    if request.method == 'POST':
        data_from_post = json.load(request)['toggle_check']
        form_parent = get_object_or_404(FormParent, pk =pk)
        # print(data_from_post)
        form_parent.accept_responses = data_from_post
        form_parent.save()

        data = {
            'toggle_value':'toggle_value',
        }
        return JsonResponse(data)
    else:
        raise Http404()

@login_required(login_url='/login_page')
def forms(request):
    form_parents = FormParent.objects.filter(builder = request.user.profile)
    context ={
        'form_parents': form_parents,
    }
    return render(request,'forms.html', context)
@login_required(login_url='/login_page')
def delete_form(request, pk):
    form_parent = get_object_or_404(FormParent, pk=pk)
    if request.user.profile == form_parent.builder:
        # print(form_parent)
        form_parent.delete()

        return redirect('/forms')
    else:
        raise Http404()


def login_page(request):
    return render(request,'login_page.html')

# def set_option(request):
#     if request.method == 'POST':
#         data_from_post = json.load(request)['option']
@login_required(login_url='/login_page')
def log_out(request):
    logout(request)
    return redirect("/")
        



