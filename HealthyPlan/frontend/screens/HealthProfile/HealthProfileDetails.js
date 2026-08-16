import { useContext } from "react";
import { ScrollView, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "../../components/AppButton";
import ScreenContainer from "../../components/ScreenContainer";
import SectionCard from "../../components/SectionCard";
import { EmptyView } from "../../components/StateViews";
import { MyUserContext } from "../../configs/Contexts";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const GENDER_LABELS = {male: "Nam", female: "Nữ"};
const ACTIVITY_LABELS = {sedentary: "Ít vận động", light: "Vận động nhẹ", moderate: "Vận động vừa", active: "Vận động nhiều", very_active: "Vận động rất nhiều"};
const GOAL_LABELS = {lose_weight: "Giảm cân", maintain_weight: "Duy trì cân nặng", gain_weight: "Tăng cân"};

const HealthProfileDetails = ({navigation}) => {
    const {healthProfile} = useContext(MyUserContext);

    if (!healthProfile) {
        return (
            <ScreenContainer withHeader>
                <EmptyView title="Chưa có hồ sơ sức khỏe" message="Hãy thiết lập hồ sơ để sử dụng các tính năng cá nhân hóa." actionTitle="Thiết lập hồ sơ" onAction={() => navigation.navigate("HealthProfileForm", {setup: true})} />
            </ScreenContainer>
        );
    }

    const DetailRow = ({label, value}) => (
        <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>{label}</Text>
            <Text style={styles.detailValue}>{value || "Chưa cập nhật"}</Text>
        </View>
    );

    return (
        <ScreenContainer withHeader>
            <ScrollView contentContainerStyle={styles.detailsScroll}>
                <SectionCard style={styles.summaryCard}>
                    <View style={styles.summaryTop}>
                        <View style={styles.summaryIcon}><Ionicons name="heart" size={28} color={Colors.primary} /></View>
                        <View>
                            <Text style={styles.summaryTitle}>Hồ sơ đã hoàn thiện</Text>
                            <Text style={styles.summaryText}>Dữ liệu đang được dùng để cá nhân hóa</Text>
                        </View>
                    </View>
                </SectionCard>
                <SectionCard title="Chỉ số và mục tiêu" icon="analytics-outline" style={styles.summaryCard}>
                    <DetailRow label="Ngày sinh" value={healthProfile.date_of_birth} />
                    <DetailRow label="Giới tính" value={GENDER_LABELS[healthProfile.gender]} />
                    <DetailRow label="Cân nặng" value={`${healthProfile.weight} kg`} />
                    <DetailRow label="Chiều cao" value={`${healthProfile.height} cm`} />
                    <DetailRow label="Mức vận động" value={ACTIVITY_LABELS[healthProfile.activity_level]} />
                    <DetailRow label="Mục tiêu" value={GOAL_LABELS[healthProfile.goal]} />
                    <DetailRow label="Cân nặng mục tiêu" value={healthProfile.target_weight ? `${healthProfile.target_weight} kg` : null} />
                </SectionCard>
                <SectionCard title="Vấn đề sức khỏe" icon="medkit-outline" style={styles.summaryCard}>
                    <View style={{flexDirection: "row", flexWrap: "wrap"}}>
                        {healthProfile.health_issues?.length > 0 ? healthProfile.health_issues.map((issue) => (
                            <View key={issue.id} style={styles.issueChip}><Text style={styles.issueChipText}>{issue.name}</Text></View>
                        )) : <Text style={styles.emptyIssues}>Chưa có vấn đề sức khỏe được gắn.</Text>}
                    </View>
                    {healthProfile.other_health_issue ? <DetailRow label="Thông tin khác" value={healthProfile.other_health_issue} /> : null}
                </SectionCard>
                <AppButton title="Cập nhật hồ sơ" icon="create-outline" onPress={() => navigation.navigate("HealthProfileForm")} />
            </ScrollView>
        </ScreenContainer>
    );
}

export default HealthProfileDetails;
