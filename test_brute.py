# Final Exam Unit Test, written by Ayden Wayman - A7W13

import pytest
import brute
import time

@pytest.fixture
def brute_simple():
    return brute.Brute("pass")

@pytest.fixture
def brute_complex():
    return brute.Brute("password1234")

@pytest.fixture
def hashed_password():
    b = brute_simple()
    return b.target
             

def describe_brute_once():
    def it_passes_correct_password():
        b = brute.Brute("password")
        assert b.bruteOnce("password") is True

    def it_fails_incorrect_password():
        b = brute.Brute("password")
        assert b.bruteOnce("incorrectpassword") is False

    def it_fails_partial_match_long():
        b = brute.Brute("password")
        assert b.bruteOnce("passwordiswrong") is False

    def it_fails_partial_match_short():
        b = brute.Brute("password")
        assert b.bruteOnce("pass") is False

    def it_matches_empty():
        b = brute.Brute("")
        assert b.bruteOnce("") is True
        assert b.bruteOnce("notempty") is False

    def it_matches_case():
        b = brute.Brute("Password")
        assert b.bruteOnce("password") is False
        assert b.bruteOnce("Password") is True

    def it_passes_with_numbers():
        b = brute.Brute("pass1234")
        assert b.bruteOnce("pass1234") is True
        assert b.bruteOnce("pass123") is False

def describe_brute_many():
    def it_returns_time_on_success(brute_simple, mocker):
        b = brute_simple
        mocker.patch.object(b, 'randomGuess', side_effect=["wrongpass", "anotherwrongpass", "thirdwrongpass", "pass"])
        result = b.bruteMany(limit=10)
        assert isinstance(result, float) and result >= 0

    def it_returns_negative_on_failure(brute_complex, mocker):
        b = brute_complex
        mocker.patch.object(b, 'randomGuess', side_effect=["wrongpass", "anotherwrongpass", "thirdwrongpass"])
        result = b.bruteMany(limit=3)
        assert result == -1

    def it_stops_at_limit(brute_simple, mocker):
        b = brute_simple
        mocker.patch.object(b, 'randomGuess', side_effect=["wrongpass", "anotherwrongpass", "thirdwrongpass", "pass"])
        result = b.bruteMany(limit=3)
        assert result == -1

    def it_does_not_iterate_with_zero_limit(brute_simple, mocker):
        b = brute_simple
        mocker.patch.object(b, 'randomGuess', side_effect=["pass"])
        result = b.bruteMany(limit=0)
        assert result == -1

    def it_stops_iterating_on_success(brute_simple, mocker):
        b = brute_simple
        mock_guess = mocker.patch.object(b, 'randomGuess', side_effect=["pass"] * 10)
        result = b.bruteMany(limit=10)
        assert result >= 0
        assert mock_guess.call_count == 1

    def it_measures_time_accurately(brute_simple, mocker):
        b = brute_simple
        mocker.patch.object(b, 'randomGuess', side_effect=["wrongpass"] * 5 + ["pass"])
        start_time = time.time()
        result = b.bruteMany(limit=10)
        end_time = time.time()
        assert result >= 0
        assert (end_time - start_time) >= result
    