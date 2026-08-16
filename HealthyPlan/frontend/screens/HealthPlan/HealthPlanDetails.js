import { useEffect, useState } from "react";
import { Alert, ScrollView, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "../../components/AppButton";
import ScreenContainer from "../../components/ScreenContainer";
import SectionCard from "../../components/SectionCard";
import StatusBadge from "../../components/StatusBadge";
import { ErrorView, LoadingView } from "../../components/StateViews";
import Apis, { endpoints, getErrorMessage } from "../../configs/Apis";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const MEAL_LABELS = {breakfast: "Bữa sáng", lunch: "Bữa trưa", dinner: "Bữa tối"};
const REVIEW_LABELS = {pending: "Chờ duyệt", approved: "Đã duyệt", rejected: "Từ chối"};
const REVIEW_TONES = {pending: "warning", approved: "success", rejected: "error"};
const STATUS_LABELS = {passed: "Đạt yêu cầu", needs_adjustment: "Cần điều chỉnh", needs_expert_review: "Cần chuyên gia xem xét", incomplete_data: "Thiếu dữ liệu", no_rules: "Chưa có quy tắc", empty_plan: "Kế hoạch trống"};
const STATUS_TONES = {passed: "success", needs_adjustment: "warning", needs_expert_review: "warning", incomplete_data: "neutral", no_rules: "neutral", empty_plan: "error"};

const getItemCalories = (item) => {
    const kcal = Number(item.food?.kcal_per_100g);
    const grams = Number(item.serving_grams);
    return Number.isFinite(kcal) && Number.isFinite(grams) ? kcal * grams / 100 : null;
}

const HealthPlanDetails = ({navigation, route}) => {
    const {planId, generationStatus} = route.params;
    const [plan, setPlan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [deleting, setDeleting] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const loadPlan = async () => {
        try {
            setLoading(true);
            setErrorMessage("");
            const response = await Apis.get(endpoints.healthPlanDetails(planId));
            setPlan(response.data);
        } catch (error) {
            setErrorMessage(getErrorMessage(error));
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadPlan();
    }, [planId]);

    const deletePlan = async () => {
        try {
            setDeleting(true);
            await Apis.delete(endpoints.healthPlanDetails(planId));
            navigation.goBack();
        } catch (error) {
            Alert.alert("Không thể xóa", getErrorMessage(error));
        } finally {
            setDeleting(false);
        }
    }

    const confirmDelete = () => {
        Alert.alert("Xóa kế hoạch", "Kế hoạch sẽ được xóa khỏi danh sách của bạn.", [
            {text: "Hủy", style: "cancel"},
            {text: "Xóa", style: "destructive", onPress: deletePlan}
        ]);
    }

    if (loading) return <ScreenContainer withHeader><LoadingView message="Đang tải chi tiết kế hoạch..." /></ScreenContainer>;
    if (errorMessage || !plan) return <ScreenContainer withHeader><ErrorView message={errorMessage || "Không tìm thấy kế hoạch."} onRetry={loadPlan} /></ScreenContainer>;

    return (
        <ScreenContainer withHeader>
            <ScrollView contentContainerStyle={styles.detailContent}>
                <View style={styles.detailHeader}>
                    <Text style={styles.detailDate}>{plan.start_date}</Text>
                    <Text style={styles.detailTitle}>{plan.title}</Text>
                    <View style={styles.badges}>
                        <StatusBadge label={REVIEW_LABELS[plan.review_status] || plan.review_status} tone={REVIEW_TONES[plan.review_status]} />
                        {generationStatus && <StatusBadge label={STATUS_LABELS[generationStatus] || generationStatus} tone={STATUS_TONES[generationStatus]} />}
                    </View>
                </View>
                {generationStatus === "needs_expert_review" && (
                    <View style={styles.statusInfo}><Ionicons name="information-circle-outline" size={20} color={Colors.warning} /><Text style={styles.statusText}>Kế hoạch được tạo thành công nhưng có quy tắc cần chuyên gia xem xét. Đây không phải lỗi hệ thống.</Text></View>
                )}
                {(plan.meals || []).map((meal) => {
                    const calories = (meal.items || []).map(getItemCalories);
                    const hasCompleteCalories = calories.length > 0 && calories.every((value) => value !== null);
                    const totalCalories = hasCompleteCalories ? calories.reduce((total, value) => total + value, 0) : null;
                    return (
                        <SectionCard key={meal.id} style={styles.mealCard}>
                            <View style={styles.mealHeader}><Text style={styles.mealTitle}>{MEAL_LABELS[meal.meal_type] || meal.meal_type}</Text><Text style={styles.mealCalories}>{totalCalories === null ? "Chưa đủ dữ liệu" : `${Math.round(totalCalories)} kcal`}</Text></View>
                            {(meal.items || []).map((item) => {
                                const calories = getItemCalories(item);
                                return (
                                    <View key={item.id} style={styles.foodRow}>
                                        <View style={styles.foodIcon}><Ionicons name="nutrition-outline" size={19} color={Colors.primary} /></View>
                                        <View style={styles.foodMain}><Text style={styles.foodName}>{item.food?.name_vi || "Thực phẩm"}</Text><Text style={styles.foodServing}>{item.serving_grams} g</Text></View>
                                        <Text style={styles.foodCalories}>{calories === null ? "--" : `${Math.round(calories)} kcal`}</Text>
                                    </View>
                                );
                            })}
                        </SectionCard>
                    );
                })}
                {plan.review_note ? <SectionCard title="Ghi chú đánh giá" icon="document-text-outline" style={styles.mealCard}><Text style={styles.reviewNote}>{plan.review_note}</Text></SectionCard> : null}
                <AppButton title="Xóa kế hoạch" icon="trash-outline" variant="danger" loading={deleting} onPress={confirmDelete} style={styles.deleteButton} />
            </ScrollView>
        </ScreenContainer>
    );
}

export default HealthPlanDetails;
