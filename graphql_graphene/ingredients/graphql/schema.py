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

    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())

    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String(),
                                notes=graphene.String())

    def resolve_all_category(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # return Ingredient.objects.select_related('category').all()
        return Ingredient.objects.all()

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id and name:
            try:
                return Category.objects.get(id=id, name=name)
            except:
                return Category.objects.none()

        if id:
            try:
                return Category.objects.get(id=id)
            except:
                return Category.objects.none()

        if name:
            try:
                return Category.objects.get(name=name)
            except:
                return Category.objects.none()

        return None


    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id and name:
            try:
                return Ingredient.objects.get(id=id, name=name)
            except:
                return Ingredient.objects.none()

        if id:
            try:
                return Ingredient.objects.get(id=id)
            except:
                return Ingredient.objects.none()

        if name:
            try:
                return Ingredient.objects.get(name=name)
            except:
                return Ingredient.objects.none()

        return None




