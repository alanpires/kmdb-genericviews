from django.test import TestCase
from rest_framework.test import APIClient
import json
import ipdb

# TESTAR FORMATO DO RETORNO DESSA VIEW
class TestMovieView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "username": "user",
            "first_name": "Edward",
            "last_name": "Stewart",
            "password": "1234",
            "is_staff": False,
            "is_superuser": False,
        }

        self.user_login_data = {"username": "user", "password": "1234"}

        self.critic_data = {
            "username": "critic",
            "first_name": "Erick",
            "last_name": "Jacquin",
            "password": "1234",
            "is_staff": True,
            "is_superuser": False,
        }

        self.critic_login_data = {"username": "critic", "password": "1234"}

        self.admin_data = {
            "username": "admin",
            "first_name": "Jeff",
            "last_name": "Bezos",
            "password": "1234",
            "is_staff": True,
            "is_superuser": True,
        }

        self.admin_login_data = {"username": "admin", "password": "1234"}

        self.movie_data = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "launch": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.movie_data_2 = {
            "title": "Um Sonho de liberdade",
            "duration": "142m",
            "genres": [{"name": "Ficção Científica"}, {"name": "Drama"}],
            "launch": "1994-10-14",
            "classification": 14,
            "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas consecutivas pelas mortes de sua esposa e de seu amante. Porém, só Andy sabe que ele não cometeu os crimes. No presídio, durante dezenove anos, ele faz amizade com Red, sofre as brutalidades da vida na cadeia, se adapta, ajuda os carcereiros, etc.",
        }

        self.movie_data_3 = {
            "title": "Em busca de liberdade",
            "duration": "175m",
            "genres": [{"name": "Obra de época"}, {"name": "Drama"}],
            "launch": "2018-02-22",
            "classification": 14,
            "synopsis": "Representando a Grã-Bretanha,  corredor Eric Liddell (Joseph Fiennes) ganha uma medalha de ouro nas Olimpíadas de Paris em 1924. Ele decide ir até a China para trabalhar como missionário e acaba encontrando um país em guerra. Com a invasão japonesa no território chinês durante a Segunda Guerra Mundial, Liddell acaba em um campo de concentração.",
        }

    def test_admin_can_create_movie(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")
        self.assertEqual(movie.json()["id"], 1)
        self.assertEqual(movie.status_code, 201)

    def test_critic_or_user_cannot_create_movie(self):
        # create critic user
        self.client.post("/api/accounts/", self.critic_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic cannot create movie
        status_code = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).status_code
        self.assertEqual(status_code, 403)

        # create user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # user cannot create movie
        status_code = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).status_code

        self.assertEqual(status_code, 403)

    def anonymous_can_list_movies(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # reset client -> no login
        client = APIClient()

        # list movies
        movies_list = client.get("/api/movies/", format="json").json()
        self.assertEqual(len(movies_list), 1)

    def test_genre_or_classification_cannot_repet(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie 1
        movie_1 = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).json()

        # create movie 2
        movie_2 = self.client.post(
            "/api/movies/", self.movie_data_2, format="json"
        ).json()
        # testa se os ids do gênero drama são os mesmos
        self.assertEqual(movie_1["genres"][1]["id"], movie_2["genres"][0]["id"])

    def test_filter_movies_with_the_filter_request(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie 1
        movie_1 = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).json()

        # create movie 2
        movie_2 = self.client.post(
            "/api/movies/", self.movie_data_2, format="json"
        ).json()

        # create movie 3
        movie_2 = self.client.post(
            "/api/movies/", self.movie_data_3, format="json"
        ).json()

        # filter movies
        filter_movies = self.client.generic(
            method="GET",
            path="/api/movies/",
            data=json.dumps({"title": "liberdade"}),
            content_type="application/json",
        )

        self.assertEqual(len(filter_movies.json()), 2)
        self.assertEqual(filter_movies.status_code, 200)


class TestMovieRetrieveDestroyView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "username": "user",
            "first_name": "Edward",
            "last_name": "Stewart",
            "password": "1234",
            "is_staff": False,
            "is_superuser": False,
        }

        self.user_login_data = {"username": "user", "password": "1234"}

        self.critic_data = {
            "username": "critic",
            "first_name": "Erick",
            "last_name": "Jacquin",
            "password": "1234",
            "is_staff": True,
            "is_superuser": False,
        }

        self.critic_login_data = {"username": "critic", "password": "1234"}

        self.admin_data = {
            "username": "admin",
            "first_name": "Jeff",
            "last_name": "Bezos",
            "password": "1234",
            "is_staff": True,
            "is_superuser": True,
        }

        self.admin_login_data = {"username": "admin", "password": "1234"}

        self.movie_data = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "launch": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.movie_data_2 = {
            "title": "Um Sonho de liberdade",
            "duration": "142m",
            "genres": [{"name": "Ficção Científica"}, {"name": "Drama"}],
            "launch": "1994-10-14",
            "classification": 14,
            "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas consecutivas pelas mortes de sua esposa e de seu amante. Porém, só Andy sabe que ele não cometeu os crimes. No presídio, durante dezenove anos, ele faz amizade com Red, sofre as brutalidades da vida na cadeia, se adapta, ajuda os carcereiros, etc.",
        }

        self.movie_data_3 = {
            "title": "Em busca de liberdade",
            "duration": "175m",
            "genres": [{"name": "Obra de época"}, {"name": "Drama"}],
            "launch": "2018-02-22",
            "classification": 14,
            "synopsis": "Representando a Grã-Bretanha,  corredor Eric Liddell (Joseph Fiennes) ganha uma medalha de ouro nas Olimpíadas de Paris em 1924. Ele decide ir até a China para trabalhar como missionário e acaba encontrando um país em guerra. Com a invasão japonesa no território chinês durante a Segunda Guerra Mundial, Liddell acaba em um campo de concentração.",
        }

    def test_anonymous_can_filter_movies(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 3 movies
        self.client.post("/api/movies/", self.movie_data, format="json")
        self.client.post("/api/movies/", self.movie_data_2, format="json")
        self.client.post("/api/movies/", self.movie_data_3, format="json")

        # reset client -> no login
        client = APIClient()

        # filter movie 1
        movies_filter = client.get("/api/movies/1/", format="json")
        self.assertEqual(movies_filter.status_code, 200)
        self.assertEqual(movies_filter.json()["id"], 1)

    def test_anonymous_cannot_filter_movies_with_the_invalid_movie_id(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 3 movies
        self.client.post("/api/movies/", self.movie_data, format="json")
        self.client.post("/api/movies/", self.movie_data_2, format="json")
        self.client.post("/api/movies/", self.movie_data_3, format="json")

        # reset client -> no login
        client = APIClient()

        # filter movie 99
        movies_filter = client.get("/api/movies/99/", format="json")
        self.assertEqual(movies_filter.status_code, 404)
        self.assertEqual(movies_filter.json(), {"detail": "Not found."})

    def test_user_or_critic_cannot_delete_movies(self):
        # create critic user
        self.client.post("/api/accounts/", self.critic_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic cannot delete movie
        status_code = self.client.delete("/api/movies/1/", format="json").status_code
        self.assertEqual(status_code, 403)

        # create user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # user cannot delete movie
        status_code = self.client.delete("/api/movies/1/", format="json").status_code
        self.assertEqual(status_code, 403)

    def test_anonymous_cannot_delete_movies(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # reset client -> no login
        client = APIClient()

        # delete movie
        movie_delete = client.delete("/api/movies/1/", format="json")
        self.assertEqual(movie_delete.status_code, 401)
        self.assertEqual(
            movie_delete.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_admin_can_delete_movie(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # get movies
        movies = self.client.get("/api/movies/", format="json")
        self.assertEqual(len(movies.json()), 1)

        # delete movie
        status_code = self.client.delete("/api/movies/1/", format="json").status_code
        self.assertEqual(status_code, 204)

        # get movies
        movies = self.client.get("/api/movies/", format="json")
        self.assertEqual(len(movies.json()), 0)
        self.assertEqual(movies.json(), [])


class TestCommentReviewView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "username": "user",
            "first_name": "Edward",
            "last_name": "Stewart",
            "password": "1234",
            "is_staff": False,
            "is_superuser": False,
        }

        self.user_login_data = {"username": "user", "password": "1234"}

        self.critic_data = {
            "username": "critic",
            "first_name": "Erick",
            "last_name": "Jacquin",
            "password": "1234",
            "is_staff": True,
            "is_superuser": False,
        }

        self.critic_login_data = {"username": "critic", "password": "1234"}

        self.admin_data = {
            "username": "admin",
            "first_name": "Jeff",
            "last_name": "Bezos",
            "password": "1234",
            "is_staff": True,
            "is_superuser": True,
        }

        self.admin_login_data = {"username": "admin", "password": "1234"}

        self.movie_data = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "launch": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.movie_data_2 = {
            "title": "Um Sonho de liberdade",
            "duration": "142m",
            "genres": [{"name": "Ficção Científica"}, {"name": "Drama"}],
            "launch": "1994-10-14",
            "classification": 14,
            "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas consecutivas pelas mortes de sua esposa e de seu amante. Porém, só Andy sabe que ele não cometeu os crimes. No presídio, durante dezenove anos, ele faz amizade com Red, sofre as brutalidades da vida na cadeia, se adapta, ajuda os carcereiros, etc.",
        }

        self.movie_data_3 = {
            "title": "Em busca de liberdade",
            "duration": "175m",
            "genres": [{"name": "Obra de época"}, {"name": "Drama"}],
            "launch": "2018-02-22",
            "classification": 14,
            "synopsis": "Representando a Grã-Bretanha,  corredor Eric Liddell (Joseph Fiennes) ganha uma medalha de ouro nas Olimpíadas de Paris em 1924. Ele decide ir até a China para trabalhar como missionário e acaba encontrando um país em guerra. Com a invasão japonesa no território chinês durante a Segunda Guerra Mundial, Liddell acaba em um campo de concentração.",
        }

        self.comment_data = {"comment": "show"}

        self.output_format_data = {
            "id": 1,
            "user": {"id": 2, "first_name": "Edward", "last_name": "Stewart"},
            "comment": "show",
        }

    def test_user_can_create_comment(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # create user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create comment on the movie
        comment = self.client.post(
            "/api/movies/1/comments/", self.comment_data, format="json"
        )

        # test output format comment data
        self.assertDictEqual(self.output_format_data, comment.json())
        self.assertEqual(comment.status_code, 201)

        # get movies
        movies = self.client.get("/api/movies/", format="json")

        # testa se o user_comments foi para o filme corretamente
        self.assertDictEqual(
            movies.json()[0]["comment_set"][0], self.output_format_data
        )

    def test_admin_or_critic_cannot_create_comment(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # admin user cannot create movie
        status_code = self.client.post(
            "/api/movies/1/comments/", self.movie_data, format="json"
        ).status_code

        self.assertEqual(status_code, 403)

        # create critic user
        self.client.post("/api/accounts/", self.critic_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic cannot create comment
        status_code = self.client.post(
            "/api/movies/1/comments/", self.comment_data, format="json"
        ).status_code
        self.assertEqual(status_code, 403)

    def test_create_comment_with_invalid_movie_id(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # create user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create comment on the movie with invalid_id
        comment = self.client.post(
            "/api/movies/99/comments/", self.comment_data, format="json"
        )

        self.assertDictEqual(comment.json(), {"detail": "Not found."})
        self.assertEqual(comment.status_code, 404)

    def test_user_can_change_a_comment_on_the_movie(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # create user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # user comment
        comment = self.client.post(
            "/api/movies/1/comments/", {"comment": "show"}, format="json"
        )

        # get movies
        movies = self.client.get("/api/movies/", format="json").json()
        self.assertEqual(movies[0]["comment_set"][0]["comment"], "show")

        comment_change = {"comment_id": 1, "comment": "fera demais!"}

        # user change a comment
        comment = self.client.put(
            "/api/movies/1/comments/", comment_change, format="json"
        )

        # get movies
        movies = self.client.get("/api/movies/", format="json").json()
        self.assertEqual(movies[0]["comment_set"][0]["comment"], "fera demais!")

    def test_user_cannot_change_a_comment_on_the_movie_that_did_not_comment(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # create user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # user comment
        self.client.post("/api/movies/1/comments/", self.comment_data, format="json")

        comment_change = {"comment_id": 1, "comment": "fera demais!"}

        # user cannot change a comment in the movie that did not comment
        comment = self.client.put(
            "/api/movies/99/comments/", comment_change, format="json"
        )

        self.assertEqual(comment.status_code, 404)
        self.assertEqual(comment.json(), {"detail": "Not found."})

        # user cannot change a comment in the movie with the invalid comment id
        comment_2 = self.client.put(
            "/api/movies/1/comments/",
            {"comment_id": 99, "comment": "fera demais!"},
            format="json",
        )

        self.assertEqual(comment_2.status_code, 404)
        self.assertEqual(comment_2.json(), {"detail": "Not found."})