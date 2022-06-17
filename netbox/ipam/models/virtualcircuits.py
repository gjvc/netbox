from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ipam.choices import L2VPNTypeChoices
from ipam.constants import L2VPN_ASSIGNMENT_MODELS
from netbox.models import NetBoxModel


class L2VPN(NetBoxModel):
    identifier = models.BigIntegerField()
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    type = models.CharField(max_length=50, choices=L2VPNTypeChoices)
    import_targets = models.ManyToManyField(
        to='ipam.RouteTarget',
        related_name='importing_l2vpns',
        blank=True,
    )
    export_targets = models.ManyToManyField(
        to='ipam.RouteTarget',
        related_name='exporting_l2vpns',
        blank=True
    )
    description = models.TextField(null=True, blank=True)
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.SET_NULL,
        related_name='l2vpns',
        blank=True,
        null=True
    )
    contacts = GenericRelation(
        to='tenancy.ContactAssignment'
    )


class L2VPNTermination(NetBoxModel):
    l2vpn = models.ForeignKey(
        to='ipam.L2VPN',
        on_delete=models.CASCADE,
        related_name='terminations',
        blank=False,
        null=False
    )

    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=L2VPN_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )

