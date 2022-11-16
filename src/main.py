import pandas as pd

from scraping import Scraping


def main():
    path = "./data/WhiskyDatabase_250.csv"
    df = pd.read_csv(path)

    scraping = Scraping()
    for key, value in df["Whisky"].items():
        print(key, value)
        count: int = 0
        max_count: int = 0
        while True:
            data = scraping.get_image(value, count)
            if data["status"]:
                # write the image path to csv file
                df.loc[key, f"image_path_{count}"] = data["image_path"]
                count += 1
            else:
                max_count += 1
            if count == 3:
                break
            if max_count == 10:
                break
        # break
    scraping.close()

    # write csv file with image path
    path = "./data/WhiskyDatabase_200_with_image.csv"
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
