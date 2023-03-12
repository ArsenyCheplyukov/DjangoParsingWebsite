import os
import re
import time
import uuid
from urllib.request import urlretrieve

from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By

from .models import *


@shared_task(bind=True)
def get_images_fit_request(self, object_id, request_text, n_images):
    """PARSE IMAGES WITH GOOGLE WEBDRIVER"""
    url_prefixes = [
        "https://www.google.com/search?source=lnms&tbm=isch&sa=X&ved=2ahUKEwiE7InesOPxAhWF_SoKHXgvCikQ_AUoAXoECAIQAw&biw=929&bih=888&q=",
        "https://yandex.ru/images/search?text=",
        "https://www.flickr.com/search/?view_all=1&text=",
        "https://www.pinterest.com/search/pins/?q=",
    ]

    # pass parameters to selenium get_element of pass False two times, scrolls until checkpoint
    click_actions = [
        [
            lambda x: x.find_element(
                By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "mye4qd", " " ))]'
            ).click(),
            50,
        ],
        [lambda x: x.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/a").click(), 50],
        [lambda x: x.find_elements(By.TAG_NAME, "button")[3].click(), 50],
        [False, 6],
    ]

    get_element_list_functions = [
        lambda x: x.find_element(By.ID, "islmp").find_elements(By.TAG_NAME, "img"),
        lambda x: x.find_elements(By.CLASS_NAME, "serp-item__thumb"),
        lambda x: x.find_element(By.CLASS_NAME, "search-photos-everyone-view")
        .find_element(By.CLASS_NAME, "photo-list-view")
        .find_elements(By.TAG_NAME, "img"),
        lambda x: x.find_element(By.ID, "mweb-unauth-container").find_elements(By.TAG_NAME, "img"),
    ]

    numbers_of_repeat = [n_images // 100, n_images // 100, n_images // 50, n_images // 10]

    save_folder = "media/photos/"

    # CHECK IS SAVE FOLDER ACTUALLY EXISTS
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    # CONFIGURE SELENIUM
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    progress_recorder = ProgressRecorder(self)

    # MAKE SET FOR FINAL URLS, REMOVE DUPLICATES
    url_data = set()

    for counted_i, unpack_staff in enumerate(
        zip(url_prefixes, click_actions, get_element_list_functions, numbers_of_repeat)
    ):
        url_prefix, click_action, get_list_function, number_of_repeat = unpack_staff
        search_url = url_prefix + request_text.strip().replace(" ", "+")
        driver.get(search_url)

        # count = 0
        # number_of_sites = len(url_prefixes)
        current_url_data = set()
        value = 0

        for counted_from_start in range(number_of_repeat):
            for _ in range(click_action[1]):
                driver.execute_script("scrollBy(" + str(value) + ", " + str(value + 200) + ");")
                value += 200
                time.sleep(0.1)
            if click_action[0] != False:
                try:
                    click_action[0](driver)
                except:
                    break
            sub = get_list_function(driver)
            time.sleep(0.2)
            for i in sub:
                try:
                    if len(current_url_data) < n_images:
                        src = i.get_attribute("src")
                        if src != None:
                            src = str(src)
                            current_url_data.add(src)
                except Exception as StaleElementReferenceException:  # catches type error along with other errors
                    break
        # print(f"\nFirst progress bar data are: {counted_i + 1} and {len(numbers_of_repeat)}\n")
        progress_recorder.set_progress(counted_i + 1, len(get_element_list_functions), f"Some text")
        # progress = (counted_from_start + 1) * 100 / number_of_repeat
        # self.update_state(state="PROGRESS", meta={"percent": progress} if progress is not None else {})
        url_data.update(current_url_data)
    driver.close()
    pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    filtered = list(filter(lambda x: re.search(pattern, x), list(url_data)))
    count = 0
    print("Enter loop")
    print("Number of images is:", len(filtered))
    for current_count, i in enumerate(filtered[:n_images]):
        slug = uuid.uuid4().hex
        # urlretrieve(i, os.path.join(save_folder, request_text.strip().replace(" ", "_") + str(count) + ".jpg"))
        # print(settings.BASE_DIR)
        try:
            result = urlretrieve(
                i,
                os.path.join(
                    settings.BASE_DIR + "search_crawl_teach/media/photos",
                    slug + ".jpg",
                ),
            )
            count += 1
            name = request_text.strip().replace(" ", "_") + str(count)
            ref_object = RequestData.objects.get(id=object_id)
            a = ImageData.objects.create(photo=f"photos/{slug}.jpg", name=name, slug=slug, request_data=ref_object)
            a.save()
        except:
            break
        progress_recorder.set_progress(current_count + 1, n_images, f"Картинка номер: {current_count+1}")
        # progress = (current_count + 1) * 100 / n_images
        # self.update_state(state="PROGRESS", meta={"percent": progress} if progress is not None else {})
