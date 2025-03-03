from django.contrib import messages
from django.http import HttpRequest, JsonResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from backend.models import Invoice


@require_http_methods(["DELETE"])
def delete_invoice(request: HttpRequest):
    delete_items = QueryDict(request.body)

    invoice = delete_items.get("invoice")

    try:
        invoice = Invoice.objects.get(id=invoice)
    except:
        return JsonResponse({"message": "Invoice not found"}, status=404)

    if not invoice.user.logged_in_as_team and invoice.user != request.user:
        return JsonResponse({"message": "You do not have permission to delete this invoice"}, status=404)

    if invoice.user.logged_in_as_team and invoice.organization != request.user.logged_in_as_team:
        return JsonResponse({"message": "You do not have permission to delete this invoice"}, status=404)

    invoice.delete()

    if request.htmx:
        messages.success(request, "Invoice deleted")
        return render(request, "base/toasts.html")

    return JsonResponse({"message": "Invoice successfully deleted"}, status=200)
