import allure

from pages.games_page import GamesPage
from pages.home_page import HomePage
from pages.jobs_page import JobsPage

home_page = HomePage()
game_page = GamesPage()
jobs_page = JobsPage()


@allure.feature("Главная")
@allure.link("https://playrix.com/", name="Main page")
def test_home_title_contains_playrix():
    home_page.should_have_title("Playrix")


@allure.feature("Саппорт")
@allure.link("https://playrix.helpshift.com/hc/ru/", name="Helpshift")
def test_go_to_support_page():
    home_page.go_to_contact().go_to_helpshift().check_helpshift_url()


@allure.feature("Вакансии")
@allure.link("https://playrix.com/job/open", name="Job page")
def test_open_job_page():
    jobs_page.open_job_page("QA").should_have_qa_jobs("QA")


@allure.feature("Страница игры на сайте")
@allure.link("https://playrix.com/games/fishdom", name="Fishdom site page")
def test_open_game_page():
    game_page.open_fishdom_page().should_have_fishdom_text_description()


@allure.feature("Страница игры в сторе")
@allure.link("https://apps.apple.com/us/app/fishdom/id664575829?mt=8", name="Fishdom store page")
def test_open_store_game_page():
    game_page.open_fishdom_page().open_store_link().should_open_app_store()


@allure.feature("Страница игры в X")
@allure.link("https://x.com/Playrix", name="Playrix X page")
def test_go_to_twitter():
    home_page.go_to_twitter().should_be_open_twitter()


@allure.feature("История компании")
@allure.link("https://playrix.com/company/history", name="Company history")
@allure.story("Проверка перехода на страницу истории компании")
@allure.severity(allure.severity_level.NORMAL)
def test_open_company_history():
    home_page.go_to_company_history().should_be_open_company_history()
