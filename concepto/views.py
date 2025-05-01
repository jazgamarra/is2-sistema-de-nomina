from django.shortcuts import render, get_object_or_404, redirect
from .models import Concepto
from .forms import ConceptoForm
from django.contrib.auth.decorators import login_required

@login_required
def listar_conceptos(request):
    conceptos = Concepto.objects.all()
    return render(request, 'concepto/listar_conceptos.html', {'conceptos': conceptos})

@login_required
def crear_concepto(request):
    if request.method == 'POST':
        form = ConceptoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_conceptos')
        else:
            print(form.errors)  # Ver errores en la consola del servidor
    else:
        form = ConceptoForm()
    return render(request, 'concepto/crear_concepto.html', {'form': form})

@login_required
def editar_concepto(request, pk):
    concepto = get_object_or_404(Concepto, pk=pk)
    if request.method == 'POST':
        form = ConceptoForm(request.POST, instance=concepto)
        if form.is_valid():
            form.save()
            return redirect('listar_conceptos')
    else:
        form = ConceptoForm(instance=concepto)
    return render(request, 'concepto/editar_concepto.html', {'form': form})

@login_required
def eliminar_concepto(request, pk):
    concepto = get_object_or_404(Concepto, pk=pk)
    if request.method == 'POST':
        concepto.delete()  # Elimina físicamente el concepto
        return redirect('listar_conceptos')
    return render(request, 'concepto/eliminar_concepto.html', {'concepto': concepto})
