import allure
from selene import browser, have, be


class HomePage:
    @allure.step('Открываем главную страницу')
    def open(self, url):
        browser.open(url)
        return self

    @allure.step("Проверить, что title содержит название")
    def should_have_title(self, text):
        browser.should(have.title_containing(text))
        return self

    @allure.step('Открыть страницу контактов из футера')
    def go_to_contact(self):
        footer = browser.element('footer')
        link = footer.all("a[href*='contact']").filtered_by(be.visible).first
        link.should(be.visible).click()
        return self

    @allure.step('Переходим в саппорт')
    def go_to_helpshift(self):
        browser.element('.support__button').click()
        return self

    @allure.step('Проверяем URL сервиса поддержки')
    def check_helpshift_url(self):
        browser.should(have.url_containing("playrix.helpshift"))
        return self

    @allure.step('Открыть страницу Twitter из футера')
    def go_to_twitter(self):
        footer = browser.element('footer')
        link = footer.all("a[href='https://twitter.com/Playrix']").filtered_by(be.visible).first
        link.should(be.visible).click()
        return self

    @allure.step('Проверить правильно ли открылась страница')
    def should_be_open_twitter(self):
        browser.should(have.url_containing("x.com"))
        browser.element("[data-testid='UserName']").should(have.text('Playrix'))

    @allure.step('Переходим на страницу истории компании')
    def go_to_company_history(self):
        # ждём появления секции "stories"
        stories_section = browser.element('.stories')
        stories_section.should(be.visible)

        # находим элемент по уникальной части класса
        link = browser.element("a.stories__item--work-history-link[href='/company/history']")
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", link())
        link.should(be.clickable).click()
        return self

    @allure.step('Проверяем, что открылась страница истории компании')
    def should_be_open_company_history(self):
        browser.should(have.url_containing("/company/history"))
        browser.element(".header-block__header.h2--large").should(be.visible)
        browser.element(".header-block__header.h2--large").should(have.text("Our journey"))
        return self
