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

    @staticmethod
    def get_queryset(cls, queryset, info):
        if info.context.user.is_anonymous:
            return queryset # Do any specific filter here
        return queryset #return super query all()


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
        if info.context.user.is_authenticated:
            return Category.objects.all()
        else:
            return None

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


class CategoryMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    def mutate(self, info, name, id):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        # Notice we return an instance of this mutation
        return CategoryMutation(category=category)


class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    # category = graphene.InputField(CategoryType)


class IngredientMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
        notes = graphene.String()
        category = CategoryInput()

    ingredient = graphene.Field(IngredientType)

    def mutate(self, info, **kwargs):
        ingredient = Ingredient.objects.get(pk=kwargs.get('id'))
        ingredient.name = kwargs.get('name', ingredient.name)
        ingredient.notes = kwargs.get('notes', ingredient.notes)
        category = kwargs.get('category', None)
        if category:
            category_id = category.get('id', None)
            category_name = category.get('name', None)

            if category_id:
                ingredient.category = Category.objects.get(pk=category_id)
                ingredient.save()

            if category_name:
                ingredient.category.name = category_name
                    # ingredient.save()

        ingredient.save()
        return IngredientMutation(ingredient=ingredient)


class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        pk = kwargs.get('id')
        Category.objects.get(pk=pk).delete()
        return DeleteCategoryMutation(ok=True)


class DeleteIngredientsMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    deleted = graphene.Boolean()

    def mutate(self, info, **kwargs):
        pk = kwargs.get('id')
        Ingredient.objects.get(pk=pk).delete()
        return DeleteCategoryMutation(deleted=True)


class CreateCategoryMutation(graphene.Mutation):
    class Arguments:
        name =  graphene.String(required=True)

    category = graphene.Field(CategoryType)

    def mutate(root, info, **kwargs):
        name = kwargs.get('name')
        category = Category(name=name)
        category.save()
        return CreateCategoryMutation(category=category)


class CreateIngredientMutation(graphene.Mutation):
    class Arguments:
        name =  graphene.String(required=True)
        notes = graphene.String(required=True)
        category = CategoryInput(required=True)

    ingredient = graphene.Field(IngredientType)

    def mutate(root, info, **kwargs):
        name = kwargs.get('name')
        notes = kwargs.get('notes')
        category = kwargs.get('category')
        category_id = category.get('id')
        category = Category.objects.get(pk=category_id)
        ingredient = Ingredient(name=name, notes=notes, category=category)
        ingredient.save()
        return CreateIngredientMutation(ingredient=ingredient)



class Mutation:
    delete_category = DeleteCategoryMutation.Field()
    delete_ingredient = DeleteIngredientsMutation.Field()

    create_category = CreateCategoryMutation.Field()
    create_ingredient = CreateIngredientMutation.Field()

    update_category = CategoryMutation.Field()
    update_ingredient = IngredientMutation.Field()

