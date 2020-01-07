# graphene imports
import graphene
from graphene_django.types import DjangoObjectType


# models import
from ingredients.models import Category, Ingredient


# Defining type for Graphql
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


# Add Type/Structure in Query
class Query(object):
    all_category = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_category(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # return Ingredient.objects.select_related('category').all()
        return Ingredient.objects.all()
