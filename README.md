# Flask-Validator-Extended
Pythonic JSON payload validator for requested JSON payload of Flask

[Flask-Validator](https://pypi.org/project/Flask-Validator/1.0/)를 확장하여, Flask를 위한 view decorator 기반의 JSON 요청 데이터 validation 라이브러리. [Flask Large Application Example](https://github.com/JoMingyu/Flask-Large-Application-Example)에서 직접 구현해 사용하던 몇 가지 view decorator에서 출발했고, [MongoEngine](https://github.com/MongoEngine/mongoengine)의 설계에 영향을 받았습니다.

- [x] View decorator for 'JSON required'(abort when mimetype is not application/json)
- [x] View decorator with Dictionary for key & type check(@validate_common)
- [x] View decorator with Iterable for key check only(@validate_keys)
- [ ] View decorator with Dictionary & Helper Fields(@validate_with_fields)
- [ ] View decorator with Validator Class & Fields likes WTForms(@validate_with_validator)
- [ ] JSON 객체의 깊이가 2 이상인 경우에 대한 고려
- [ ] 테스트&CI 붙이기
