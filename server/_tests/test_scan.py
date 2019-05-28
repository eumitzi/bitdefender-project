from workers.scan import detect


def test_detect():
    the_file = {
        "oh": {"ep": 0},
        "fh": {"ns": "1"},
        "md5": "foo",
        "sec": [{"va": 100, "s": 10, "n": "sec_name"}],
    }
    result = detect({"buffers": [the_file]})
    assert result == None
