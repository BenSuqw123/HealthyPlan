import { useState } from "react";
import { KeyboardAvoidingView, Platform, ScrollView, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "../../components/AppButton";
import AppTextInput from "../../components/AppTextInput";
import DateInput from "../../components/DateInput";
import ScreenContainer from "../../components/ScreenContainer";
import SectionCard from "../../components/SectionCard";
import Apis, { endpoints, getErrorMessage, getFieldError, requireResponseData } from "../../configs/Apis";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const getToday = () => {
    const date = new Date();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${date.getFullYear()}-${month}-${day}`;
}

const GeneratePlan = ({navigation}) => {
    const [planDate, setPlanDate] = useState(getToday());
    const [title, setTitle] = useState("");
    const [errors, setErrors] = useState({});
    const [errorMessage, setErrorMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const submit = async () => {
        if (!planDate || loading) {
            if (!planDate) setErrors({...errors, plan_date: "Vui lòng chọn ngày."});
            return;
        }

        try {
            setLoading(true);
            setErrorMessage("");
            const payload = {plan_date: planDate};
            if (title.trim()) payload.title = title.trim();
            const response = await Apis.post(endpoints.generateMealPlan, payload, {timeout: 60000});
            const result = requireResponseData(response, "Máy chủ không trả về kế hoạch vừa tạo.");
            if (!result.health_plan?.id) {
                const error = new Error("Phản hồi tạo kế hoạch không có mã kế hoạch.");
                error.userMessage = error.message;
                throw error;
            }
            navigation.replace("HealthPlanDetails", {planId: result.health_plan.id, generationStatus: result.status});
        } catch (error) {
            setErrors({plan_date: getFieldError(error, "plan_date"), title: getFieldError(error, "title")});
            setErrorMessage(getErrorMessage(error));
        } finally {
            setLoading(false);
        }
    }

    return (
        <ScreenContainer withHeader>
            <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={{flex: 1}}>
                <ScrollView keyboardShouldPersistTaps="handled" contentContainerStyle={styles.formScroll}>
                    <View style={styles.formIntro}><Text style={styles.formTitle}>Tạo thực đơn một ngày</Text><Text style={styles.formDescription}>HealthyPlan sẽ chọn thực phẩm thật từ dữ liệu Backend và điều chỉnh theo hồ sơ sức khỏe.</Text></View>
                    {errorMessage ? <View style={styles.errorBox}><Text style={styles.errorText}>{errorMessage}</Text></View> : null}
                    <SectionCard title="Thông tin kế hoạch" icon="calendar-outline" style={styles.formCard}>
                        <DateInput label="Ngày áp dụng" value={planDate} minimumDate={getToday()} error={errors.plan_date} onChange={(value) => {setPlanDate(value); setErrors({...errors, plan_date: null});}} />
                        <AppTextInput label="Tiêu đề (không bắt buộc)" icon="create-outline" maxLength={255} value={title} error={errors.title} onChangeText={(value) => {setTitle(value); setErrors({...errors, title: null});}} placeholder="Ví dụ: Thực đơn ngày làm việc" />
                    </SectionCard>
                    <View style={styles.noteBox}><Ionicons name="information-circle-outline" size={20} color={Colors.primary} /><Text style={styles.noteText}>Mỗi ngày chỉ có một kế hoạch ăn uống đang hoạt động. Quá trình tạo có thể mất vài giây.</Text></View>
                    <AppButton title="Tạo kế hoạch" icon="sparkles-outline" loading={loading} disabled={loading} onPress={submit} />
                </ScrollView>
            </KeyboardAvoidingView>
        </ScreenContainer>
    );
}

export default GeneratePlan;
