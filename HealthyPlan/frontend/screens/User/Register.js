import { useState } from "react";
import { Alert, KeyboardAvoidingView, Platform, Pressable, ScrollView, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "../../components/AppButton";
import AppTextInput from "../../components/AppTextInput";
import ScreenContainer from "../../components/ScreenContainer";
import Apis, { endpoints, getErrorMessage, getFieldError } from "../../configs/Apis";
import styles from "./Style";

const Register = ({navigation}) => {
    const [user, setUser] = useState({username: "", email: "", first_name: "", last_name: "", password: "", password_confirm: ""});
    const [errors, setErrors] = useState({});
    const [errorMessage, setErrorMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const changeField = (field, value) => {
        setUser({...user, [field]: value});
        setErrors({...errors, [field]: null});
    }

    const validate = () => {
        const nextErrors = {};
        if (!user.username.trim()) nextErrors.username = "Vui lòng nhập tên đăng nhập.";
        if (!user.email.trim()) nextErrors.email = "Vui lòng nhập email.";
        if (!user.password) nextErrors.password = "Vui lòng nhập mật khẩu.";
        if (!user.password_confirm) nextErrors.password_confirm = "Vui lòng xác nhận mật khẩu.";
        if (user.password && user.password_confirm && user.password !== user.password_confirm) nextErrors.password_confirm = "Mật khẩu xác nhận không khớp.";
        setErrors(nextErrors);
        return Object.keys(nextErrors).length === 0;
    }

    const submit = async () => {
        if (!validate() || loading) return;

        try {
            setLoading(true);
            setErrorMessage("");
            await Apis.post(endpoints.users, {
                username: user.username.trim(),
                email: user.email.trim(),
                first_name: user.first_name.trim(),
                last_name: user.last_name.trim(),
                password: user.password,
                password_confirm: user.password_confirm
            });
            Alert.alert("Đăng ký thành công", "Bạn có thể đăng nhập bằng tài khoản vừa tạo.", [{text: "Đăng nhập", onPress: () => navigation.replace("Login")}]);
        } catch (error) {
            setErrors({
                username: getFieldError(error, "username"),
                email: getFieldError(error, "email"),
                password: getFieldError(error, "password"),
                password_confirm: getFieldError(error, "password_confirm")
            });
            setErrorMessage(getErrorMessage(error));
        } finally {
            setLoading(false);
        }
    }

    return (
        <ScreenContainer>
            <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={{flex: 1}}>
                <ScrollView keyboardShouldPersistTaps="handled" contentContainerStyle={styles.authScroll}>
                    <View style={styles.brand}>
                        <View style={styles.brandIcon}><Ionicons name="leaf" size={38} color="#FFFFFF" /></View>
                        <Text style={styles.brandName}>Tạo tài khoản</Text>
                        <Text style={styles.subtitle}>Bắt đầu xây dựng lối sống phù hợp với bạn</Text>
                    </View>
                    <View style={styles.formCard}>
                        {errorMessage ? <Text style={styles.generalError}>{errorMessage}</Text> : null}
                        <AppTextInput autoCapitalize="words" error={errors.first_name} icon="person-outline" label="Tên" onChangeText={(text) => changeField("first_name", text)} placeholder="Tên của bạn" value={user.first_name} />
                        <AppTextInput autoCapitalize="words" error={errors.last_name} icon="people-outline" label="Họ và tên lót" onChangeText={(text) => changeField("last_name", text)} placeholder="Họ và tên lót" value={user.last_name} />
                        <AppTextInput autoCapitalize="none" autoCorrect={false} error={errors.username} icon="at-outline" label="Tên đăng nhập" onChangeText={(text) => changeField("username", text)} placeholder="Tên đăng nhập" value={user.username} />
                        <AppTextInput autoCapitalize="none" error={errors.email} icon="mail-outline" keyboardType="email-address" label="Email" onChangeText={(text) => changeField("email", text)} placeholder="email@example.com" value={user.email} />
                        <AppTextInput error={errors.password} icon="lock-closed-outline" label="Mật khẩu" onChangeText={(text) => changeField("password", text)} placeholder="Nhập mật khẩu" secureTextEntry value={user.password} />
                        <AppTextInput error={errors.password_confirm} icon="shield-checkmark-outline" label="Xác nhận mật khẩu" onChangeText={(text) => changeField("password_confirm", text)} onSubmitEditing={submit} placeholder="Nhập lại mật khẩu" secureTextEntry value={user.password_confirm} />
                        <AppButton title="Đăng ký" icon="person-add-outline" loading={loading} onPress={submit} />
                    </View>
                    <View style={styles.footerRow}>
                        <Text style={styles.footerText}>Đã có tài khoản?</Text>
                        <Pressable accessibilityRole="button" onPress={() => navigation.goBack()}><Text style={styles.footerLink}>Đăng nhập</Text></Pressable>
                    </View>
                </ScrollView>
            </KeyboardAvoidingView>
        </ScreenContainer>
    );
}

export default Register;
