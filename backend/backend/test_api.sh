#!/bin/bash

# FastAPI Authentication Backend - Automated API Testing Script
# This script tests all API endpoints and validates responses

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API_URL="http://localhost:8000"
TEST_EMAIL="testuser$(date +%s)@example.com"
TEST_USERNAME="testuser$(date +%s)"
TEST_PASSWORD="TestPass123!"

# Counters
PASSED=0
FAILED=0

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

print_test() {
    echo -e "${YELLOW}▶ Testing:${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓ PASS:${NC} $1"
    ((PASSED++))
}

print_error() {
    echo -e "${RED}✗ FAIL:${NC} $1"
    ((FAILED++))
}

print_info() {
    echo -e "${BLUE}ℹ Info:${NC} $1"
}

wait_for_api() {
    print_info "Waiting for API to be ready..."
    for i in {1..30}; do
        if curl -s "$API_URL/health" > /dev/null 2>&1; then
            print_success "API is ready!"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    print_error "API did not start in time"
    exit 1
}

# Test 1: Health Check
test_health() {
    print_test "Health Check Endpoint"
    
    response=$(curl -s -w "\n%{http_code}" "$API_URL/health")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        print_success "Health check returned 200 OK"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        print_error "Health check failed with code $http_code"
    fi
}

# Test 2: Root Endpoint
test_root() {
    print_test "Root Endpoint"
    
    response=$(curl -s -w "\n%{http_code}" "$API_URL/")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        print_success "Root endpoint returned 200 OK"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        print_error "Root endpoint failed with code $http_code"
    fi
}

# Test 3: User Registration
test_registration() {
    print_test "User Registration"
    
    response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/register" \
        -H "Content-Type: application/json" \
        -d "{
            \"email\": \"$TEST_EMAIL\",
            \"username\": \"$TEST_USERNAME\",
            \"password\": \"$TEST_PASSWORD\"
        }")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "201" ]; then
        print_success "User registration successful (201 Created)"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        print_error "User registration failed with code $http_code"
        echo "$body"
    fi
}

# Test 4: Duplicate Email Registration
test_duplicate_registration() {
    print_test "Duplicate Email Registration (should fail)"
    
    response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/register" \
        -H "Content-Type: application/json" \
        -d "{
            \"email\": \"$TEST_EMAIL\",
            \"username\": \"another_user\",
            \"password\": \"$TEST_PASSWORD\"
        }")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "400" ]; then
        print_success "Duplicate registration correctly rejected (400 Bad Request)"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        print_error "Duplicate registration not handled correctly (expected 400, got $http_code)"
        echo "$body"
    fi
}

# Test 5: Weak Password Registration
test_weak_password() {
    print_test "Weak Password Registration (should fail)"
    
    response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/register" \
        -H "Content-Type: application/json" \
        -d "{
            \"email\": \"weak@example.com\",
            \"username\": \"weakuser\",
            \"password\": \"weak\"
        }")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "422" ]; then
        print_success "Weak password correctly rejected (422 Unprocessable Entity)"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        print_error "Weak password not handled correctly (expected 422, got $http_code)"
        echo "$body"
    fi
}

# Test 6: User Login
test_login() {
    print_test "User Login"
    
    response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/login" \
        -H "Content-Type: application/json" \
        -d "{
            \"email\": \"$TEST_EMAIL\",
            \"password\": \"$TEST_PASSWORD\"
        }")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        print_success "User login successful (200 OK)"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
        
        # Extract token for next tests
        ACCESS_TOKEN=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
        
        if [ -n "$ACCESS_TOKEN" ]; then
            print_info "JWT token extracted successfully"
        else
            print_error "Failed to extract JWT token"
        fi
    else
        print_error "User login failed with code $http_code"
        echo "$body"
    fi
}

# Test 7: Login with Wrong Password
test_wrong_password() {
    print_test "Login with Wrong Password (should fail)"
    
    response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/login" \
        -H "Content-Type: application/json" \
        -d "{
            \"email\": \"$TEST_EMAIL\",
            \"password\": \"WrongPassword123!\"
        }")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "401" ]; then
        print_success "Wrong password correctly rejected (401 Unauthorized)"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        print_error "Wrong password not handled correctly (expected 401, got $http_code)"
        echo "$body"
    fi
}

# Test 8: Protected Endpoint with Valid Token
test_protected_valid_token() {
    print_test "Protected Endpoint with Valid Token"
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "No access token available. Skipping test."
        return
    fi
    
    response=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/users/me" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        print_success "Protected endpoint accessed successfully (200 OK)"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        print_error "Protected endpoint failed with code $http_code"
        echo "$body"
    fi
}

# Test 9: Protected Endpoint without Token
test_protected_no_token() {
    print_test "Protected Endpoint without Token (should fail)"
    
    response=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/users/me")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "403" ]; then
        print_success "No token correctly rejected (403 Forbidden)"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        print_error "No token not handled correctly (expected 403, got $http_code)"
        echo "$body"
    fi
}

# Test 10: Protected Endpoint with Invalid Token
test_protected_invalid_token() {
    print_test "Protected Endpoint with Invalid Token (should fail)"
    
    response=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/users/me" \
        -H "Authorization: Bearer invalid_token_12345")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "401" ]; then
        print_success "Invalid token correctly rejected (401 Unauthorized)"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        print_error "Invalid token not handled correctly (expected 401, got $http_code)"
        echo "$body"
    fi
}

# Test 11: API Documentation
test_docs() {
    print_test "API Documentation (Swagger)"
    
    response=$(curl -s -w "\n%{http_code}" "$API_URL/docs")
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "200" ]; then
        print_success "Swagger documentation accessible (200 OK)"
    else
        print_error "Swagger documentation failed with code $http_code"
    fi
}

# Main execution
main() {
    print_header "FastAPI Authentication Backend - API Testing"
    
    print_info "API URL: $API_URL"
    print_info "Test Email: $TEST_EMAIL"
    print_info "Test Username: $TEST_USERNAME"
    
    # Wait for API to be ready
    wait_for_api
    
    # Run all tests
    print_header "Running Tests"
    
    test_health
    echo ""
    
    test_root
    echo ""
    
    test_registration
    echo ""
    
    test_duplicate_registration
    echo ""
    
    test_weak_password
    echo ""
    
    test_login
    echo ""
    
    test_wrong_password
    echo ""
    
    test_protected_valid_token
    echo ""
    
    test_protected_no_token
    echo ""
    
    test_protected_invalid_token
    echo ""
    
    test_docs
    echo ""
    
    # Summary
    print_header "Test Summary"
    
    TOTAL=$((PASSED + FAILED))
    echo -e "${BLUE}Total Tests:${NC} $TOTAL"
    echo -e "${GREEN}Passed:${NC} $PASSED"
    echo -e "${RED}Failed:${NC} $FAILED"
    echo ""
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  ✓ ALL TESTS PASSED!${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        exit 0
    else
        echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
        echo -e "${RED}  ✗ SOME TESTS FAILED${NC}"
        echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
        exit 1
    fi
}

# Run main function
main