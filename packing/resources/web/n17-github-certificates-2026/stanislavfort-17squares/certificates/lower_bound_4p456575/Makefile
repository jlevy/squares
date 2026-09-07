CXX ?= g++
CXXFLAGS ?= -O3 -std=c++17 -Wall -Wextra -pedantic
CERT := square17_lb_4p456575.cert
all: generate_certificate verify_certificate verify_certificate_bigint
generate_certificate: generate_certificate.cpp lower_bound_common.hpp
	$(CXX) $(CXXFLAGS) -o $@ generate_certificate.cpp
verify_certificate: verify_certificate.cpp lower_bound_common.hpp
	$(CXX) $(CXXFLAGS) -o $@ verify_certificate.cpp
verify_certificate_bigint: verify_certificate_bigint.cpp
	$(CXX) $(CXXFLAGS) -o $@ verify_certificate_bigint.cpp
check: all
	./verify_certificate $(CERT)
	./verify_certificate_bigint $(CERT)
	python3 verify_certificate.py $(CERT)
regenerate: generate_certificate
	./generate_certificate $(CERT).new
	./verify_certificate_bigint $(CERT).new
clean:
	rm -f generate_certificate verify_certificate verify_certificate_bigint $(CERT).new
