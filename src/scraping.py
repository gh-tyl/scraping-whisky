import base64
import time
import traceback

from selenium import webdriver


class Scraping:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--ignore-ssl-errors=yes")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=self.options)
        self.timer = 1
        self.wait = 10

    def get_image(self, key: str, count: int) -> dict:
        try:
            self.driver.get("https://www.google.com")
            self.driver.implicitly_wait(self.wait)
            search = self.driver.find_element("name", "q")
            search.send_keys(key)
            search.submit()
            self.driver.implicitly_wait(self.wait)
        except:
            traceback.print_exc()
            # refresh the driver
            self.refresh()
            return {"status": False, "image_path": None}
        # open image tab
        try:
            # open the image tab
            tab_num: int = 4
            for num in range(2, tab_num):
                tab_path = f'//*[@id="hdtb-msb"]/div[1]/div/div[{num}]/a'
                tab = self.driver.find_element("xpath", tab_path)
                # get innerText
                tab_text = tab.get_attribute("innerText")
                if tab_text == "Images":
                    time.sleep(self.timer)
                    tab.click()
                    self.driver.implicitly_wait(self.wait)
                    break
        except:
            traceback.print_exc()
            # refresh the driver
            self.refresh()
            return {"status": False, "image_path": None}
        try:
            time.sleep(self.timer)
            # get the first image
            image = self.driver.find_element(
                "xpath", f'//*[@id="islrg"]/div[1]/div[{count+1}]/a[1]/div[1]/img'
            )
            image_url = image.get_attribute("src")
            # download the data:image/jpeg;base64,
            image_data = image_url.split(",")[1]
            # decode the base64
            image_data = image_data.encode("utf-8")
            image_data = base64.b64decode(image_data)
            # save the image
            # replace the space with underscore
            key_name = key.replace(" ", "_")
            image_path = "data/images/" + key_name + "_" + str(count) + ".jpg"
            with open(image_path, "wb") as f:
                f.write(image_data)
            # refresh the page
            return {"status": True, "image_path": image_path}
        except Exception as e:
            traceback.print_exc()
            # refresh the driver
            self.refresh()
            return {"status": False, "image_path": None}

    def close(self):
        # close the tab
        self.driver.close()
        # close the browser
        self.driver.quit()

    def refresh(self):
        self.driver.quit()
        self.driver = webdriver.Chrome(options=self.options)


if __name__ == "__main__":
    scraping = Scraping()
    for count in range(3):
        data = scraping.get_image("Sullivans Cove Bourbon Cask Strength", count)
    scraping.close()
