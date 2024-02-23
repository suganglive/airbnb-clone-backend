from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "name",
            "kind",
        )


# class CategorySerializer(serializers.Serializer):

#     pk = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(
#         required=True,
#         max_length=150,
#     )
#     kind = serializers.ChoiceField(
#         choices=Category.CategoryKindChoices.choices,
#     )
#     created_at = serializers.DateTimeField(read_only=True)

#     # when serializer.save() happens in views.py.//, create function will called and run.
#     def create(self, validated_data):
#         return Category.objects.create(**validated_data)
#         ## ** operator -> dictionary({'name':"adkjfklasj"}) to name = "adkjfklasj"

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.kind = validated_data.get("kind", instance.kind)
#         instance.save()
#         return instance
