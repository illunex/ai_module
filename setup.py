import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ai module",  # 프로젝트 이름
    version="0.1.13",  # 프로젝트 버전
    description="Modules related to preprocessing, crawling, collection, database, data load & save ",  # 간단한 설명
    url="https://github.com/illunex/ai_module",  # 프로젝트 주소
    author="jhkang",  # 작성자
    author_email="jhkang@illunex.com",  # 작성자 이메일
    long_description=long_description,  # 프로젝트 설명, 보통 README.md로 관리
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[  # 설치시 설치할 라이브러리
        "sqlalchemy",
        "webdriver_manager",
        "selenium",
        "openpyxl",
        "pandas"
    ],
)
