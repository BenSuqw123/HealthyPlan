import { useContext, useState } from "react";
import { KeyboardAvoidingView, Platform, ScrollView, Text } from "react-native";

import AppButton from "../../components/AppButton";
import AppTextInput from "../../components/AppTextInput";
import ScreenContainer from "../../components/ScreenContainer";
import Apis, { endpoints, getErrorMessage, getFieldError, requireResponseData } from "../../configs/Apis";
import { MyUserContext } from "../../configs/Contexts";
import styles from "./Style";

const UpdateUser = ({navigation}) => {
    const {user, updateUser} = useContext(MyUserContext);
    const [form, setForm] = useState({email: user?.email || "", first_name: user?.first_name || "", last_name: user?.last_name || ""});
    const [errors, setErrors] = useState({});
    const [errorMessage, setErrorMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const changeField = (field, value) => {
        setForm({...form, [field]: value});
        setErrors({...errors, [field]: null});
    }

    const submit = async () => {
        if (!form.email.trim()) {
            setErrors({...errors, email: "Vui lòng nhập email."});
            return;
        }

        try {
            setLoading(true);
            setErrorMessage("");
            const response = await Apis.patch(endpoints.currentUser, {email: form.email.trim(), first_name: form.first_name.trim(), last_name: form.last_name.trim()});
            updateUser(requireResponseData(response, "Máy chủ không trả về thông tin tài khoản đã cập nhật."));
            navigation.goBack();
        } catch (error) {
            setErrors({email: getFieldError(error, "email"), first_name: getFieldError(error, "first_name"), last_name: getFieldError(error, "last_name")});
            setErrorMessage(getErrorMessage(error));
        } finally {
            setLoading(false);
        }
    }

    return (
        <ScreenContainer withHeader>
            <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={{flex: 1}}>
                <ScrollView keyboardShouldPersistTaps="handled" contentContainerStyle={styles.updateScroll}>
                    {errorMessage ? <Text style={styles.generalError}>{errorMessage}</Text> : null}
                    <AppTextInput autoCapitalize="words" error={errors.first_name} icon="person-outline" label="Tên" onChangeText={(text) => changeField("first_name", text)} value={form.first_name} />
                    <AppTextInput autoCapitalize="words" error={errors.last_name} icon="people-outline" label="Họ và tên lót" onChangeText={(text) => changeField("last_name", text)} value={form.last_name} />
                    <AppTextInput autoCapitalize="none" error={errors.email} icon="mail-outline" keyboardType="email-address" label="Email" onChangeText={(text) => changeField("email", text)} value={form.email} />
                    <AppButton title="Lưu thay đổi" icon="checkmark-circle-outline" loading={loading} onPress={submit} />
                </ScrollView>
            </KeyboardAvoidingView>
        </ScreenContainer>
    );
}

export default UpdateUser;
