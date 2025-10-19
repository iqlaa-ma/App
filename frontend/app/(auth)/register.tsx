import { router } from 'expo-router';
import { useState } from 'react';
import {
  Image,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';



export default function Register() {
  const [password, setPassword] = useState('');
  const [focusedInput, setFocusedInput] = useState(null);

  // Calculate password strength
  const getPasswordStrength = (pass) => {
    if (!pass) return 0;
    let strength = 0;
    if (pass.length >= 6) strength++;
    if (pass.length >= 10) strength++;
    if (/[a-z]/.test(pass) && /[A-Z]/.test(pass)) strength++;
    if (/\d/.test(pass)) strength++;
    if (/[^a-zA-Z\d]/.test(pass)) strength++;
    return strength;
  };

  const strength = getPasswordStrength(password);
  const getStrengthColor = () => {
    if (strength >= 4) return '#14B8A6';
    if (strength >= 2) return '#F59E0B';
    return '#EF4444';
  };
  const getStrengthLabel = () => {
    if (strength >= 4) return 'Strong';
    if (strength >= 2) return 'Medium';
    return 'Weak';
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView
        style={styles.keyboardView}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          {/* Back Button */}
          <TouchableOpacity 
            style={styles.backButton}
            onPress={() => router.back()}
          >
            <Text style={styles.backButtonText}>← Back</Text>
          </TouchableOpacity>

          {/* Logo */}
          <View style={styles.logoContainer}>
            <Image 
              source={require('../../assets/logos/iqlaalogo.png')}
              style={styles.logo}
              resizeMode="contain"
            />
          </View>

          {/* Title */}
          <Text style={styles.title}>Get Started Free</Text>
          
          {/* Subtitle */}
          <Text style={styles.subtitle}>Free Forever. No Credit Card Needed</Text>
          
          {/* Email Address Input */}
          <View style={styles.inputWrapper}>
            <Text style={styles.label}>Email Adress</Text>
            <View style={[
              styles.inputContainer,
              focusedInput === 'email' && styles.inputContainerFocused
            ]}>
              <View style={styles.iconContainer}>
                <Text style={styles.icon}>✉️</Text>
              </View>
              <TextInput
                style={styles.input}
                placeholder="yourname@gmail.com"
                placeholderTextColor="#6B7280"
                keyboardType="email-address"
                autoCapitalize="none"
                onFocus={() => setFocusedInput('email')}
                onBlur={() => setFocusedInput(null)}
              />
            </View>
          </View>
          
          {/* Your Name Input */}
          <View style={styles.inputWrapper}>
            <Text style={styles.label}>Your Name</Text>
            <View style={[
              styles.inputContainer,
              focusedInput === 'name' && styles.inputContainerFocused
            ]}>
              <View style={styles.iconContainer}>
                <Text style={styles.icon}>👤</Text>
              </View>
              <TextInput
                style={styles.input}
                placeholder="@yourname"
                placeholderTextColor="#6B7280"
                autoCapitalize="none"
                onFocus={() => setFocusedInput('name')}
                onBlur={() => setFocusedInput(null)}
              />
            </View>
          </View>
          
          {/* Password Input */}
          <View style={styles.inputWrapper}>
            <Text style={styles.label}>Password</Text>
            <View style={[
              styles.inputContainer,
              focusedInput === 'password' && styles.inputContainerFocused
            ]}>
              <View style={styles.iconContainer}>
                <Text style={styles.icon}>🔑</Text>
              </View>
              <TextInput
                style={styles.input}
                placeholder="••••••••••"
                placeholderTextColor="#6B7280"
                secureTextEntry
                value={password}
                onChangeText={setPassword}
                onFocus={() => setFocusedInput('password')}
                onBlur={() => setFocusedInput(null)}
              />
              {/* Password Strength Indicator */}
              {password.length > 0 && (
                <View style={styles.strengthIndicator}>
                  <View style={styles.strengthBars}>
                    <View style={[styles.strengthBar, { backgroundColor: strength >= 1 ? getStrengthColor() : '#2A3340' }]} />
                    <View style={[styles.strengthBar, { backgroundColor: strength >= 2 ? getStrengthColor() : '#2A3340' }]} />
                    <View style={[styles.strengthBar, { backgroundColor: strength >= 3 ? getStrengthColor() : '#2A3340' }]} />
                  </View>
                  <Text style={[styles.strengthText, { color: getStrengthColor() }]}>
                    {getStrengthLabel()}
                  </Text>
                </View>
              )}
            </View>
          </View>
          
          {/* Sign Up Button */}
          <TouchableOpacity
            style={styles.signUpButton}
            onPress={() => router.push('/home')}
          >
            <Text style={styles.signUpButtonText}>Sign up</Text>
          </TouchableOpacity>
          
          {/* Divider */}
          <View style={styles.dividerContainer}>
            <View style={styles.divider} />
            <Text style={styles.dividerText}>Or sign up with</Text>
            <View style={styles.divider} />
          </View>
          
          {/* Social Sign Up Buttons */}
          <View style={styles.socialContainer}>
            <TouchableOpacity style={styles.socialButton}>
              <Text style={styles.socialIconText}>G</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.socialButton}>
              <Text style={styles.socialIconText}>🍎</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.socialButton}>
              <Text style={styles.socialIconText}>f</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0A0E14',
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
    paddingVertical: 20,
  },
  backButton: {
    alignSelf: 'flex-start',
    marginBottom: 20,
    paddingVertical: 8,
  },
  backButtonText: {
    color: '#14B8A6',
    fontSize: 16,
    fontWeight: '600',
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  logo: {
    width: 120,
    height: 120,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 8,
    color: '#FFFFFF',
  },
  subtitle: {
    textAlign: 'center',
    color: '#9CA3AF',
    marginBottom: 40,
    fontSize: 14,
  },
  inputWrapper: {
    marginBottom: 20,
    width: '100%',
  },
  label: {
    color: '#FFFFFF',
    marginBottom: 8,
    fontSize: 14,
    fontWeight: '400',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1A1F2B',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#2A3340',
    paddingHorizontal: 12,
    minHeight: 56,
  },
  inputContainerFocused: {
    borderColor: '#14B8A6',
    borderWidth: 1.5,
  },
  iconContainer: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  icon: {
    fontSize: 20,
    color: '#6B7280',
  },
  input: {
    flex: 1,
    color: '#FFFFFF',
    paddingVertical: 14,
    fontSize: 16,
  },
  strengthIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingLeft: 8,
  },
  strengthBars: {
    flexDirection: 'row',
    gap: 4,
  },
  strengthBar: {
    width: 16,
    height: 4,
    borderRadius: 2,
  },
  strengthText: {
    fontSize: 12,
    fontWeight: '600',
  },
  signUpButton: {
    backgroundColor: '#14B8A6',
    padding: 16,
    borderRadius: 12,
    marginTop: 8,
    marginBottom: 24,
    width: '100%',
  },
  signUpButtonText: {
    color: '#FFFFFF',
    textAlign: 'center',
    fontSize: 18,
    fontWeight: '600',
  },
  dividerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
  },
  divider: {
    flex: 1,
    height: 1,
    backgroundColor: '#2A3340',
  },
  dividerText: {
    color: '#6B7280',
    paddingHorizontal: 16,
    fontSize: 13,
  },
  socialContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 16,
    marginBottom: 32,
  },
  socialButton: {
    width: 64,
    height: 64,
    backgroundColor: '#1A1F2B',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#2A3340',
    justifyContent: 'center',
    alignItems: 'center',
  },
  socialIconText: {
    fontSize: 24,
    color: '#FFFFFF',
    fontWeight: '600',
  },
});
