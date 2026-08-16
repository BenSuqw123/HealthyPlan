import { useCallback, useState } from "react";
import { FlatList, Pressable, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";
import { useFocusEffect } from "@react-navigation/native";

import ScreenContainer from "../../components/ScreenContainer";
import StatusBadge from "../../components/StatusBadge";
import { EmptyView, ErrorView, LoadingView } from "../../components/StateViews";
import Apis, { endpoints, getErrorMessage } from "../../configs/Apis";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const REVIEW_LABELS = {pending: "Chờ duyệt", approved: "Đã duyệt", rejected: "Từ chối"};
const REVIEW_TONES = {pending: "warning", approved: "success", rejected: "error"};

const HealthPlans = ({navigation}) => {
    const [plans, setPlans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const loadPlans = async (refresh = false) => {
        try {
            refresh ? setRefreshing(true) : setLoading(true);
            setErrorMessage("");
            const response = await Apis.get(endpoints.healthPlans);
            const responsePlans = Array.isArray(response.data) ? response.data : [];
            responsePlans.sort((first, second) => second.start_date.localeCompare(first.start_date));
            setPlans(responsePlans);
        } catch (error) {
            setErrorMessage(getErrorMessage(error));
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    }

    useFocusEffect(useCallback(() => {
        loadPlans();
    }, []));

    const renderPlan = ({item}) => {
        const [, month, day] = item.start_date.split("-");
        return (
            <Pressable onPress={() => navigation.navigate("HealthPlanDetails", {planId: item.id})} style={styles.planCard}>
                <View style={styles.planTop}>
                    <View style={styles.dateBox}><Text style={styles.dateDay}>{day}</Text><Text style={styles.dateMonth}>THÁNG {month}</Text></View>
                    <View style={styles.planMain}>
                        <Text numberOfLines={2} style={styles.planTitle}>{item.title}</Text>
                        <Text style={styles.planDate}>{item.start_date}</Text>
                    </View>
                    <Ionicons name="chevron-forward" size={20} color={Colors.textSecondary} />
                </View>
                <View style={styles.planBottom}>
                    <Text style={styles.mealCount}>{item.meals?.length || 0} bữa ăn</Text>
                    <StatusBadge label={REVIEW_LABELS[item.review_status] || item.review_status} tone={REVIEW_TONES[item.review_status]} />
                </View>
            </Pressable>
        );
    }

    if (loading && plans.length === 0) return <ScreenContainer><LoadingView message="Đang tải kế hoạch..." /></ScreenContainer>;
    if (errorMessage && plans.length === 0) return <ScreenContainer><ErrorView message={errorMessage} onRetry={loadPlans} /></ScreenContainer>;

    return (
        <ScreenContainer>
            <FlatList
                data={plans}
                keyExtractor={(item) => String(item.id)}
                renderItem={renderPlan}
                refreshing={refreshing}
                onRefresh={() => loadPlans(true)}
                contentContainerStyle={[styles.listContent, plans.length === 0 && {flex: 1}]}
                ListHeaderComponent={
                    <View style={styles.listHeader}>
                        <View style={styles.titleRow}>
                            <View style={styles.titleBlock}><Text style={styles.title}>Kế hoạch ăn uống</Text><Text style={styles.subtitle}>Thực đơn một ngày được cá nhân hóa theo hồ sơ của bạn.</Text></View>
                            <Pressable accessibilityLabel="Tạo kế hoạch" onPress={() => navigation.navigate("GeneratePlan")} style={styles.createButton}><Ionicons name="add" size={27} color={Colors.surface} /></Pressable>
                        </View>
                    </View>
                }
                ListEmptyComponent={<EmptyView title="Chưa có kế hoạch" message="Tạo kế hoạch ăn uống đầu tiên cho một ngày của bạn." actionTitle="Tạo kế hoạch" onAction={() => navigation.navigate("GeneratePlan")} />}
            />
        </ScreenContainer>
    );
}

export default HealthPlans;
