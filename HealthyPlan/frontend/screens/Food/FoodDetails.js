import { useEffect, useState } from "react";
import { ScrollView, Text, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import ScreenContainer from "../../components/ScreenContainer";
import SectionCard from "../../components/SectionCard";
import { ErrorView, LoadingView } from "../../components/StateViews";
import Apis, { endpoints, getErrorMessage } from "../../configs/Apis";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const ITEM_TYPE_LABELS = {raw_ingredient: "Nguyên liệu thô", cooked_food: "Thực phẩm đã nấu", basic_food: "Thực phẩm cơ bản", beverage: "Đồ uống", prepared_food: "Thực phẩm chế biến sẵn"};
const PROCESSING_LABELS = {unprocessed: "Chưa chế biến", minimally_processed: "Chế biến tối thiểu", processed: "Đã chế biến"};

const FoodDetails = ({route}) => {
    const {foodId} = route.params;
    const [food, setFood] = useState(null);
    const [loading, setLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState("");

    const loadFood = async () => {
        try {
            setLoading(true);
            setErrorMessage("");
            const response = await Apis.get(endpoints.foodDetails(foodId));
            setFood(response.data);
        } catch (error) {
            setErrorMessage(getErrorMessage(error));
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadFood();
    }, [foodId]);

    if (loading) return <ScreenContainer withHeader><LoadingView message="Đang tải thông tin dinh dưỡng..." /></ScreenContainer>;
    if (errorMessage || !food) return <ScreenContainer withHeader><ErrorView message={errorMessage || "Không tìm thấy thực phẩm."} onRetry={loadFood} /></ScreenContainer>;

    const NutritionRow = ({name, value, unit}) => (
        <View style={styles.nutritionRow}>
            <Text style={styles.nutritionName}>{name}</Text>
            <Text style={styles.nutritionValue}>{value === null || value === undefined ? "Chưa có dữ liệu" : `${value} ${unit}`}</Text>
        </View>
    );

    return (
        <ScreenContainer withHeader>
            <ScrollView contentContainerStyle={styles.detailContent}>
                <View style={styles.detailHero}>
                    <View style={styles.heroIcon}><Ionicons name="nutrition" size={31} color={Colors.surface} /></View>
                    <Text style={styles.detailName}>{food.name_vi}</Text>
                    {food.name_en ? <Text style={styles.detailEnglish}>{food.name_en}</Text> : null}
                    <View style={styles.detailMeta}>
                        <View style={styles.metaChip}><Text style={styles.metaText}>{food.category_vi}</Text></View>
                        <View style={styles.metaChip}><Text style={styles.metaText}>{ITEM_TYPE_LABELS[food.item_type] || food.item_type}</Text></View>
                        <View style={styles.metaChip}><Text style={styles.metaText}>{PROCESSING_LABELS[food.processing_level] || food.processing_level}</Text></View>
                    </View>
                </View>
                <SectionCard title="Dinh dưỡng trên 100 g" icon="analytics-outline" style={styles.nutritionCard}>
                    <NutritionRow name="Năng lượng" value={food.kcal_per_100g} unit="kcal" />
                    <NutritionRow name="Protein" value={food.protein_g} unit="g" />
                    <NutritionRow name="Chất béo" value={food.fat_g} unit="g" />
                    <NutritionRow name="Carbohydrate" value={food.carb_g} unit="g" />
                    <NutritionRow name="Chất xơ" value={food.fiber_g} unit="g" />
                    <NutritionRow name="Natri" value={food.sodium_mg} unit="mg" />
                    <NutritionRow name="Kali" value={food.potassium_mg} unit="mg" />
                    <NutritionRow name="Chất béo bão hòa" value={food.saturated_fat_g} unit="g" />
                </SectionCard>
                <SectionCard title="Nguồn dữ liệu" icon="library-outline"><Text style={styles.sourceText}>{food.source_name} · Mã thực phẩm: {food.food_id}</Text></SectionCard>
            </ScrollView>
        </ScreenContainer>
    );
}

export default FoodDetails;
