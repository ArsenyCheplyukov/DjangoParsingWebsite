import os
import re
import time
import uuid
from urllib.request import urlretrieve

from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.conf import settings
from django.dispatch import Signal

# from django_celery_progressbar.bars import ProgressBar
from selenium import webdriver
from selenium.webdriver.common.by import By

# Define a signal that will be fired to update the task status
task_update = Signal()

from .models import *


@shared_task(bind=True)
def get_images_fit_request(self, object_id, request_text, n_images):
    """PARSE IMAGES WITH GOOGLE WEBDRIVER"""
    total_work_to_do = 100
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

    save_folder = os.path.join(settings.MEDIA_ROOT, "photos")

    # CHECK IS SAVE FOLDER ACTUALLY EXISTS
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    # CONFIGURE SELENIUM
    options = webdriver.ChromeOptions()
    options.headless = True  # False
    # driver = webdriver.Chrome(options=options)
    print("Went into driver")
    if os.path.exists("/proc/self/cgroup") and "docker" in open("/proc/self/cgroup").read():
        # Running inside a Docker container
        driver = webdriver.Remote(command_executor="http://chrome:4444/wd/hub", options=options)
    else:
        # Running outside a Docker container
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

        progress_recorder.set_progress(((counted_i + 1) * 50) // len(numbers_of_repeat), total_work_to_do)
        url_data.update(current_url_data)
    driver.close()
    pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    filtered = list(filter(lambda x: re.search(pattern, x), list(url_data)))
    # print(filtered, "\n", os.path.join(str(settings.BASE_DIR), save_folder))
    count = 0
    for current_count, i in enumerate(filtered[:n_images]):
        slug = uuid.uuid4().hex
        try:
            result = urlretrieve(
                i,
                os.path.join(
                    save_folder,
                    slug + ".jpg",
                ),
            )
            count += 1
            name = request_text.strip().replace(" ", "_") + str(count)
            # print(f"The object id is: {object_id}")
            ref_object = RequestData.objects.get(id=object_id)
            # print(f"Query to find data status: {1 if ref_object else 0}")
            a = ImageData.objects.create(
                photo=os.path.join(save_folder, f"{slug}.jpg"), name=name, slug=slug, request_data=ref_object
            )
            print(f'The path of downloaded image is: {os.path.join(save_folder, f"{slug}.jpg")}')
            a.save()
        except Exception as e:
            # print(str(e))
            break

        asd = len(filtered)

        # print(str(asd) + " " + str(current_count))

        progress_recorder.set_progress(((counted_i + 1) * 50) // len(numbers_of_repeat) + 50, total_work_to_do)
