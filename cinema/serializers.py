from rest_framework import serializers
from .models import Genre, Actor, Movie, CinemaHall, MovieSession


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ActorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name", "full_name"]

    @staticmethod
    def get_full_name(obj):
        return f"{obj.first_name} {obj.last_name}"


class CinemaHallSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = CinemaHall
        fields = ["id", "name", "rows", "seats_in_row", "capacity"]


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "duration", "genres", "actors"]


class MovieListSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    actors = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "duration", "genres", "actors"]

    @staticmethod
    def get_actors(obj):
        return [f"{actor.first_name} {actor.last_name}"
                for actor in obj.actors.all()]


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "duration", "genres", "actors"]

    @staticmethod
    def get_genres(obj):
        return [genre.name for genre in obj.genres.all()]

    @staticmethod
    def get_actors(obj):
        return [f"{actor.first_name} {actor.last_name}"
                for actor in obj.actors.all()]


class MovieSessionSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    cinema_hall_name = serializers.CharField(source="cinema_hall.name",
                                             read_only=True)
    cinema_hall_capacity = serializers.IntegerField(
        source="cinema_hall.capacity", read_only=True
    )

    class Meta:
        model = MovieSession
        fields = [
            "id",
            "show_time",
            "movie",
            "cinema_hall",
            "movie_title",
            "cinema_hall_name",
            "cinema_hall_capacity",
        ]

    @staticmethod
    def validate_show_time(value):
        from django.utils import timezone

        if timezone.is_naive(value):
            value = timezone.make_aware(value)
        return value


class MovieSessionDetailSerializer(serializers.ModelSerializer):
    movie = MovieDetailSerializer(read_only=True)
    cinema_hall = CinemaHallSerializer(read_only=True)

    class Meta:
        model = MovieSession
        fields = ["id", "show_time", "movie", "cinema_hall"]
