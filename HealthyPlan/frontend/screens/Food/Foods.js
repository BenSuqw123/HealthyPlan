import { useEffect, useRef, useState } from "react";
import { ActivityIndicator, FlatList, Pressable, Text, TextInput, View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import AppButton from "../../components/AppButton";
import AppTextInput from "../../components/AppTextInput";
import ChoiceField from "../../components/ChoiceField";
import ScreenContainer from "../../components/ScreenContainer";
import { EmptyView, ErrorView, LoadingView } from "../../components/StateViews";
import Apis, { endpoints, getErrorMessage } from "../../configs/Apis";
import { Colors } from "../../configs/Theme";
import styles from "./Style";

const ITEM_TYPES = [
    {value: "", label: "Tất cả"},
    {value: "raw_ingredient", label: "Nguyên liệu thô"},
    {value: "cooked_food", label: "Đã nấu"},
    {value: "basic_food", label: "Cơ bản"},
    {value: "beverage", label: "Đồ uống"},
    {value: "prepared_food", label: "Chế biến sẵn"}
];
const PROCESSING_LEVELS = [
    {value: "", label: "Tất cả"},
    {value: "unprocessed", label: "Chưa chế biến"},
    {value: "minimally_processed", label: "Tối thiểu"},
    {value: "processed", label: "Đã chế biến"}
];

const formatNutrient = (value, suffix) => value === null || value === undefined ? "--" : `${Number(value).toFixed(1)}${suffix}`;

const Foods = ({navigation}) => {
    const [foods, setFoods] = useState([]);
    const [search, setSearch] = useState("");
    const [itemType, setItemType] = useState("");
    const [processingLevel, setProcessingLevel] = useState("");
    const [categoryInput, setCategoryInput] = useState("");
    const [category, setCategory] = useState("");
    const [filtersVisible, setFiltersVisible] = useState(false);
    const [page, setPage] = useState(1);
    const [hasMore, setHasMore] = useState(false);
    const [total, setTotal] = useState(0);
    const [loading, setLoading] = useState(true);
    const [loadingMore, setLoadingMore] = useState(false);
    const [refreshing, setRefreshing] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [loadMoreError, setLoadMoreError] = useState("");
    const loadingMoreRef = useRef(false);
    const activeQueryRef = useRef("");

    const getQueryKey = () => JSON.stringify({search: search.trim(), itemType, processingLevel, category});

    const loadFoods = async (targetPage = 1, mode = "initial") => {
        const queryKey = getQueryKey();
        if (targetPage === 1) activeQueryRef.current = queryKey;

        try {
            if (mode === "refresh") setRefreshing(true);
            else if (targetPage > 1) {setLoadingMore(true); loadingMoreRef.current = true;}
            else setLoading(true);
            if (targetPage > 1) setLoadMoreError("");
            else {setErrorMessage(""); setLoadMoreError("");}

            const params = {page: targetPage, page_size: 20};
            if (search.trim()) params.search = search.trim();
            if (itemType) params.item_type = itemType;
            if (processingLevel) params.processing_level = processingLevel;
            if (category) params.category_vi = category;

            const response = await Apis.get(endpoints.foods, {params});
            if (activeQueryRef.current !== queryKey) return;

            const responseFoods = Array.isArray(response.data?.results) ? response.data.results : [];
            setTotal(Number(response.data?.count || 0));
            setHasMore(Boolean(response.data?.next));
            setPage(targetPage);
            setFoods((current) => {
                if (targetPage === 1) return responseFoods;
                const foodMap = new Map(current.map((food) => [food.id, food]));
                responseFoods.forEach((food) => foodMap.set(food.id, food));
                return Array.from(foodMap.values());
            });
        } catch (error) {
            if (activeQueryRef.current === queryKey) {
                if (targetPage > 1) setLoadMoreError(getErrorMessage(error));
                else setErrorMessage(getErrorMessage(error));
            }
        } finally {
            if (activeQueryRef.current === queryKey) {
                setLoading(false);
                setRefreshing(false);
                setLoadingMore(false);
                loadingMoreRef.current = false;
            }
        }
    }

    useEffect(() => {
        activeQueryRef.current = getQueryKey();
        const timer = setTimeout(() => loadFoods(1), 450);
        return () => clearTimeout(timer);
    }, [search, itemType, processingLevel, category]);

    const loadMore = () => {
        if (hasMore && !loading && !loadingMoreRef.current) loadFoods(page + 1, "more");
    }

    const resetFilters = () => {
        setItemType("");
        setProcessingLevel("");
        setCategoryInput("");
        setCategory("");
    }

    const renderFood = ({item}) => (
        <Pressable onPress={() => navigation.navigate("FoodDetails", {foodId: item.id})} style={styles.foodCard}>
            <View style={styles.foodTop}>
                <View style={styles.foodIcon}><Ionicons name="nutrition-outline" size={24} color={Colors.primary} /></View>
                <View style={styles.foodMain}>
                    <Text numberOfLines={2} style={styles.foodName}>{item.name_vi}</Text>
                    {item.name_en ? <Text numberOfLines={1} style={styles.foodEnglish}>{item.name_en}</Text> : null}
                </View>
                <Ionicons name="chevron-forward" size={19} color={Colors.textSecondary} />
            </View>
            <Text style={styles.category}>{item.category_vi}</Text>
            <View style={styles.nutrients}>
                <View style={styles.nutrient}><Text style={styles.nutrientValue}>{formatNutrient(item.kcal_per_100g, "")}</Text><Text style={styles.nutrientLabel}>kcal</Text></View>
                <View style={styles.nutrient}><Text style={styles.nutrientValue}>{formatNutrient(item.protein_g, "g")}</Text><Text style={styles.nutrientLabel}>Đạm</Text></View>
                <View style={styles.nutrient}><Text style={styles.nutrientValue}>{formatNutrient(item.fat_g, "g")}</Text><Text style={styles.nutrientLabel}>Béo</Text></View>
                <View style={styles.nutrient}><Text style={styles.nutrientValue}>{formatNutrient(item.carb_g, "g")}</Text><Text style={styles.nutrientLabel}>Carb</Text></View>
            </View>
        </Pressable>
    );

    const header = (
        <View style={styles.header}>
            <Text style={styles.title}>Tra cứu thực phẩm</Text>
            <Text style={styles.subtitle}>Dữ liệu dinh dưỡng thật từ hệ thống HealthyPlan.</Text>
            <View style={styles.searchRow}>
                <View style={styles.searchBox}>
                    <Ionicons name="search-outline" size={20} color={Colors.textSecondary} />
                    <TextInput autoCapitalize="none" autoCorrect={false} onChangeText={setSearch} placeholder="Tên tiếng Việt, tiếng Anh hoặc mã..." placeholderTextColor={Colors.disabled} style={styles.searchInput} value={search} />
                    {search ? <Pressable accessibilityLabel="Xóa tìm kiếm" onPress={() => setSearch("")}><Ionicons name="close-circle" size={19} color={Colors.textSecondary} /></Pressable> : null}
                </View>
                <Pressable accessibilityLabel="Bộ lọc" onPress={() => setFiltersVisible(!filtersVisible)} style={styles.filterButton}><Ionicons name="options-outline" size={23} color={Colors.surface} /></Pressable>
            </View>
            {filtersVisible && (
                <View style={styles.filters}>
                    <ChoiceField horizontal label="Loại thực phẩm" options={ITEM_TYPES} value={itemType} onChange={setItemType} />
                    <ChoiceField horizontal label="Mức chế biến" options={PROCESSING_LEVELS} value={processingLevel} onChange={setProcessingLevel} />
                    <AppTextInput label="Danh mục tiếng Việt (khớp chính xác)" value={categoryInput} onChangeText={setCategoryInput} placeholder="Ví dụ: Ngũ cốc" />
                    <View style={styles.filterActions}>
                        <AppButton title="Đặt lại" variant="outline" onPress={resetFilters} style={styles.filterAction} />
                        <AppButton title="Áp dụng" onPress={() => setCategory(categoryInput.trim())} style={styles.filterAction} />
                    </View>
                </View>
            )}
            {errorMessage && foods.length > 0 ? <View style={styles.inlineError}><Text style={styles.inlineErrorText}>{errorMessage}</Text><Pressable onPress={() => loadFoods(1)}><Text style={styles.retryText}>Thử lại</Text></Pressable></View> : null}
            <Text style={styles.resultText}>{total.toLocaleString("vi-VN")} kết quả</Text>
        </View>
    );

    if (loading && foods.length === 0) return <ScreenContainer><LoadingView message="Đang tải dữ liệu thực phẩm..." /></ScreenContainer>;
    if (errorMessage && foods.length === 0) return <ScreenContainer><ErrorView message={errorMessage} onRetry={() => loadFoods(1)} /></ScreenContainer>;

    return (
        <ScreenContainer>
            <FlatList
                data={foods}
                keyExtractor={(item) => String(item.id)}
                renderItem={renderFood}
                ListHeaderComponent={header}
                ListEmptyComponent={<EmptyView title="Không tìm thấy thực phẩm" message="Hãy đổi từ khóa hoặc bộ lọc rồi thử lại." />}
                ListFooterComponent={loadingMore ? <ActivityIndicator style={styles.footer} color={Colors.primary} /> : loadMoreError ? <View style={styles.loadMoreError}><Text style={styles.inlineErrorText}>{loadMoreError}</Text><Pressable onPress={() => loadFoods(page + 1, "more")}><Text style={styles.retryText}>Tải lại trang tiếp theo</Text></Pressable></View> : null}
                contentContainerStyle={[styles.list, foods.length === 0 && {flexGrow: 1}]}
                onEndReached={loadMore}
                onEndReachedThreshold={0.35}
                onRefresh={() => loadFoods(1, "refresh")}
                refreshing={refreshing}
                keyboardShouldPersistTaps="handled"
            />
        </ScreenContainer>
    );
}

export default Foods;
