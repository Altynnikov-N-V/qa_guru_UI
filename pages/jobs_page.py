import allure
from selene import browser, have, be


class JobsPage:
    @allure.step("Открываем страницу поиска работы: {job}")
    def open_job_page(self, job):
        browser.element("a[href*='/job']").hover()
        browser.element("a[href*='/job/open']").click()
        browser.all(".tags-list__name").by(have.exact_text(job)).first.click()
        return self

    @allure.step('Проверяем работу фильтра')
    def should_have_qa_jobs(self, job):
        browser.element('.jobs-card__section-name').should(have.text(job))
        return self
