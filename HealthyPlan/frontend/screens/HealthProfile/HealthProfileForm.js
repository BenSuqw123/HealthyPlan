import { useContext, useEffect, useState } from "react";
import { ActivityIndicator, KeyboardAvoidingView, Platform, Pressable, ScrollView, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "../../components/AppButton";
import AppTextInput from "../../components/AppTextInput";
import ChoiceField from "../../components/ChoiceField";
import DateInput from "../../components/DateInput";
import ScreenContainer from "../../components/ScreenContainer";
import SectionCard from "../../components/SectionCard";
import Apis, { endpoints, getErrorMessage, getFieldError, requireResponseData } from "../../configs/Apis";
import { MyUserContext } from "../../configs/Contexts";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const GENDER_OPTIONS = [{value: "male", label: "Nam"}, {value: "female", label: "Nữ"}];
const ACTIVITY_OPTIONS = [
    {value: "sedentary", label: "Ít vận động"},
    {value: "light", label: "Vận động nhẹ"},
    {value: "moderate", label: "Vận động vừa"},
    {value: "active", label: "Vận động nhiều"},
    {value: "very_active", label: "Vận động rất nhiều"}
];
const GOAL_OPTIONS = [
    {value: "lose_weight", label: "Giảm cân"},
    {value: "maintain_weight", label: "Duy trì cân nặng"},
    {value: "gain_weight", label: "Tăng cân"}
];

const today = () => {
    const date = new Date();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${date.getFullYear()}-${month}-${day}`;
}

const createInitialForm = (profile) => ({
    date_of_birth: profile?.date_of_birth || "",
    gender: profile?.gender || "male",
    weight: profile?.weight || "",
    height: profile?.height || "",
    activity_level: profile?.activity_level || "moderate",
    goal: profile?.goal || "maintain_weight",
    target_weight: profile?.target_weight || "",
    other_health_issue: profile?.other_health_issue || ""
});

const HealthProfileForm = ({navigation, route}) => {
    const {healthProfile, updateHealthProfile} = useContext(MyUserContext);
    const setup = route?.params?.setup === true || !healthProfile;
    const [form, setForm] = useState(createInitialForm(healthProfile));
    const [healthIssues, setHealthIssues] = useState([]);
    const [issuesLoading, setIssuesLoading] = useState(true);
    const [issuesError, setIssuesError] = useState("");
    const [errors, setErrors] = useState({});
    const [errorMessage, setErrorMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const loadHealthIssues = async () => {
        try {
            setIssuesLoading(true);
            setIssuesError("");
            const response = await Apis.get(endpoints.healthIssues);
            setHealthIssues(Array.isArray(response.data) ? response.data : []);
        } catch (error) {
            setIssuesError(getErrorMessage(error));
        } finally {
            setIssuesLoading(false);
        }
    }

    useEffect(() => {
        loadHealthIssues();
    }, []);

    const changeField = (field, value) => {
        setForm({...form, [field]: value});
        setErrors({...errors, [field]: null, non_field_errors: null});
    }

    const validate = () => {
        const nextErrors = {};
        if (!form.date_of_birth) nextErrors.date_of_birth = "Vui lòng chọn ngày sinh.";
        if (!form.weight || Number(form.weight) <= 0) nextErrors.weight = "Cân nặng phải lớn hơn 0.";
        if (!form.height || Number(form.height) <= 0) nextErrors.height = "Chiều cao phải lớn hơn 0.";
        if (form.goal !== "maintain_weight" && (!form.target_weight || Number(form.target_weight) <= 0)) nextErrors.target_weight = "Vui lòng nhập cân nặng mục tiêu.";
        if (form.goal === "lose_weight" && Number(form.target_weight) >= Number(form.weight)) nextErrors.target_weight = "Mục tiêu giảm cân phải nhỏ hơn cân nặng hiện tại.";
        if (form.goal === "gain_weight" && Number(form.target_weight) <= Number(form.weight)) nextErrors.target_weight = "Mục tiêu tăng cân phải lớn hơn cân nặng hiện tại.";
        setErrors(nextErrors);
        return Object.keys(nextErrors).length === 0;
    }

    const submit = async () => {
        if (!validate() || loading) return;

        const payload = {
            date_of_birth: form.date_of_birth,
            gender: form.gender,
            weight: form.weight,
            height: form.height,
            activity_level: form.activity_level,
            goal: form.goal,
            target_weight: form.goal === "maintain_weight" ? form.weight : form.target_weight,
            other_health_issue: form.other_health_issue.trim() || null
        };

        try {
            setLoading(true);
            setErrorMessage("");
            const response = healthProfile
                ? await Apis.patch(endpoints.currentProfile, payload)
                : await Apis.post(endpoints.healthProfiles, payload);
            updateHealthProfile(requireResponseData(response, "Máy chủ không trả về hồ sơ sức khỏe đã lưu."));
            if (!setup && navigation.canGoBack()) navigation.goBack();
        } catch (error) {
            setErrors({
                date_of_birth: getFieldError(error, "date_of_birth"),
                gender: getFieldError(error, "gender"),
                weight: getFieldError(error, "weight"),
                height: getFieldError(error, "height"),
                activity_level: getFieldError(error, "activity_level"),
                goal: getFieldError(error, "goal"),
                target_weight: getFieldError(error, "target_weight"),
                other_health_issue: getFieldError(error, "other_health_issue")
            });
            setErrorMessage(getErrorMessage(error));
        } finally {
            setLoading(false);
        }
    }

    const selectedIssueIds = new Set((healthProfile?.health_issues || []).map((issue) => issue.id));

    return (
        <ScreenContainer withHeader={!setup}>
            <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={{flex: 1}}>
                <ScrollView keyboardShouldPersistTaps="handled" contentContainerStyle={styles.scroll}>
                    <View style={styles.setupHeader}>
                        {setup && <View style={styles.setupBadge}><Text style={styles.setupBadgeText}>BƯỚC THIẾT LẬP</Text></View>}
                        <Text style={styles.title}>{healthProfile ? "Cập nhật hồ sơ sức khỏe" : "Hiểu rõ sức khỏe của bạn"}</Text>
                        <Text style={styles.description}>Thông tin này giúp HealthyPlan cá nhân hóa kế hoạch ăn uống và nội dung tư vấn.</Text>
                    </View>
                    {errorMessage ? <View style={styles.errorBox}><Text style={styles.errorText}>{errorMessage}</Text></View> : null}

                    <SectionCard title="Thông tin cơ bản" icon="person-outline" style={styles.section}>
                        <DateInput label="Ngày sinh" value={form.date_of_birth} maximumDate={today()} error={errors.date_of_birth} onChange={(value) => changeField("date_of_birth", value)} />
                        <ChoiceField label="Giới tính" options={GENDER_OPTIONS} value={form.gender} error={errors.gender} onChange={(value) => changeField("gender", value)} />
                        <AppTextInput label="Cân nặng hiện tại (kg)" icon="scale-outline" keyboardType="decimal-pad" value={String(form.weight)} error={errors.weight} onChangeText={(value) => changeField("weight", value)} />
                        <AppTextInput label="Chiều cao (cm)" icon="resize-outline" keyboardType="decimal-pad" value={String(form.height)} error={errors.height} onChangeText={(value) => changeField("height", value)} />
                    </SectionCard>

                    <SectionCard title="Mức vận động và mục tiêu" icon="walk-outline" style={styles.section}>
                        <ChoiceField label="Mức vận động" options={ACTIVITY_OPTIONS} value={form.activity_level} error={errors.activity_level} onChange={(value) => changeField("activity_level", value)} />
                        <ChoiceField label="Mục tiêu" options={GOAL_OPTIONS} value={form.goal} error={errors.goal} onChange={(value) => changeField("goal", value)} />
                        {form.goal !== "maintain_weight" && <AppTextInput label="Cân nặng mục tiêu (kg)" icon="flag-outline" keyboardType="decimal-pad" value={String(form.target_weight)} error={errors.target_weight} onChangeText={(value) => changeField("target_weight", value)} />}
                    </SectionCard>

                    <SectionCard title="Vấn đề sức khỏe" icon="medkit-outline" style={styles.section}>
                        <View style={styles.infoBox}>
                            <Ionicons name="information-circle-outline" size={20} color={Colors.primary} />
                            <Text style={styles.infoText}>API hiện chỉ cho phép đọc danh mục và các vấn đề đã gắn với hồ sơ. Khi Backend hỗ trợ field ghi, danh sách này mới có thể chỉnh sửa an toàn.</Text>
                        </View>
                        {issuesLoading ? <ActivityIndicator color={Colors.primary} /> : issuesError ? (
                            <View><Text style={styles.issuesError}>{issuesError}</Text><Pressable onPress={loadHealthIssues}><Text style={styles.retryText}>Thử tải lại</Text></Pressable></View>
                        ) : healthIssues.map((issue) => (
                            <View key={issue.id} style={styles.issueRow}>
                                <View style={styles.issueHeader}>
                                    <Text style={styles.issueName}>{issue.name}</Text>
                                    {selectedIssueIds.has(issue.id) && <View style={styles.selectedTag}><Text style={styles.selectedTagText}>Đã chọn</Text></View>}
                                </View>
                                {issue.parent_name ? <Text style={styles.issueParent}>Thuộc: {issue.parent_name}</Text> : null}
                            </View>
                        ))}
                        <AppTextInput label="Vấn đề sức khỏe khác" multiline value={form.other_health_issue} error={errors.other_health_issue} onChangeText={(value) => changeField("other_health_issue", value)} placeholder="Mô tả thêm nếu cần" />
                    </SectionCard>
                    <AppButton title={healthProfile ? "Lưu thay đổi" : "Hoàn tất hồ sơ"} icon="checkmark-circle-outline" loading={loading} onPress={submit} />
                </ScrollView>
            </KeyboardAvoidingView>
        </ScreenContainer>
    );
}

export default HealthProfileForm;
