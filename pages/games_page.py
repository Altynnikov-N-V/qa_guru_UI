import allure
from selene import browser, have, be


class GamesPage:
    @allure.step('Отрываем страницу Fishdom')
    def open_fishdom_page(self):
        browser.element("a.main-menu__link[href='/games']").click()
        browser.element('a.game--fishdom.games-list__item').should(be.visible).click()
        return self

    @allure.step('Проверяем переход на страницу Fishdom')
    def should_have_fishdom_text_description(self):
        browser.element('.header-block__header').should(have.text('Fishdom'))
        return self

    @allure.step('Переходим на страницу игры в сторе')
    def open_store_link(self):
        browser.element("a.application-stores__item[href*='apple']").should(be.visible).click()
        return self

    @allure.step('Проверяем стор и игру, на которую ведет ссылка')
    def should_open_app_store(self):
        browser.should(have.url_containing('apps.apple.com'))
        browser.element("svelte-1bm25t").should(have.text("Fishdom"))
        return self
