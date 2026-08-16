import { useContext, useState } from "react";
import { KeyboardAvoidingView, Platform, Pressable, ScrollView, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "../../components/AppButton";
import AppTextInput from "../../components/AppTextInput";
import ScreenContainer from "../../components/ScreenContainer";
import { MyUserContext } from "../../configs/Contexts";
import { getErrorMessage } from "../../configs/Apis";
import styles from "./Style";

const Login = ({navigation}) => {
    const {login} = useContext(MyUserContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errors, setErrors] = useState({});
    const [errorMessage, setErrorMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const validate = () => {
        const nextErrors = {};
        if (!username.trim()) nextErrors.username = "Vui lòng nhập tên đăng nhập.";
        if (!password) nextErrors.password = "Vui lòng nhập mật khẩu.";
        setErrors(nextErrors);
        return Object.keys(nextErrors).length === 0;
    }

    const submit = async () => {
        if (!validate() || loading) return;

        try {
            setLoading(true);
            setErrorMessage("");
            await login(username.trim(), password);
        } catch (error) {
            const message = error.response?.data?.error === "invalid_grant"
                ? "Tên đăng nhập hoặc mật khẩu chưa đúng."
                : getErrorMessage(error);
            setErrorMessage(message);
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
                        <Text style={styles.brandName}>HealthyPlan</Text>
                        <Text style={styles.subtitle}>Đồng hành cùng mục tiêu sức khỏe của bạn mỗi ngày</Text>
                    </View>
                    <View style={styles.formCard}>
                        <Text style={styles.formTitle}>Chào mừng trở lại</Text>
                        <Text style={styles.formDescription}>Đăng nhập để tiếp tục kế hoạch cá nhân của bạn.</Text>
                        {errorMessage ? <Text style={styles.generalError}>{errorMessage}</Text> : null}
                        <AppTextInput
                            autoCapitalize="none"
                            autoCorrect={false}
                            error={errors.username}
                            icon="person-outline"
                            label="Tên đăng nhập"
                            onChangeText={(text) => {setUsername(text); setErrors({...errors, username: null});}}
                            placeholder="Nhập tên đăng nhập"
                            returnKeyType="next"
                            value={username}
                        />
                        <AppTextInput
                            error={errors.password}
                            icon="lock-closed-outline"
                            label="Mật khẩu"
                            onChangeText={(text) => {setPassword(text); setErrors({...errors, password: null});}}
                            onSubmitEditing={submit}
                            placeholder="Nhập mật khẩu"
                            returnKeyType="done"
                            secureTextEntry
                            value={password}
                        />
                        <AppButton title="Đăng nhập" icon="log-in-outline" loading={loading} onPress={submit} />
                    </View>
                    <View style={styles.footerRow}>
                        <Text style={styles.footerText}>Chưa có tài khoản?</Text>
                        <Pressable accessibilityRole="button" onPress={() => navigation.navigate("Register")}>
                            <Text style={styles.footerLink}>Đăng ký</Text>
                        </Pressable>
                    </View>
                </ScrollView>
            </KeyboardAvoidingView>
        </ScreenContainer>
    );
}

export default Login;
